from http import HTTPStatus
import logging
from utils.random_utils import RandomUtils
from utils.file_utils import FileUtils
from py_selenium_auto.browsers.browser_services import BrowserServices
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.disk_page import DiskPage
from steps.login_steps import LoginSteps
from pages.docviewer_page import DocViewerPage
from pages.image_page import ImagePage
from utils.image_utils import ImageUtils
from utils.browser_utils import BrowserUtils
from models.upload_link import UploadLink
from models.resource_meta import TrashListResponse
from enums.trash_sort import TrashSort

logger = logging.getLogger(__name__)


class TestDiskApi:
    def test_disk_api(self, config, test_data, disk_api):
        logger.info("Step 1: open main page")
        settings = BrowserServices.Instance.service_provider.settings_file()
        start_url = settings.get("startUrl")
        BrowserServices.Instance.browser.go_to(start_url)
        main_page = MainPage()

        assert main_page.state.wait_for_displayed(), (
            f"{main_page.name} is not opened"
        )

        logger.info("Step 2: go to login page and fill login form")
        main_page.click_login()

        login_page = LoginPage()
        assert login_page.state.wait_for_displayed(), (
            f"{login_page.name} is not opened"
        )

        login_steps = LoginSteps(login_page)
        login_steps.fill_login_form(config.email, config.password)

        disk_page = DiskPage()
        assert disk_page.state.wait_for_displayed(), (
            f"{disk_page.name} is not opened"
        )

        logger.info("Step 3: use API to upload text file with random text")
        base_name = RandomUtils.generate_string_field(
            test_data.text_content_length)

        text_content = RandomUtils.generate_string_field(
            test_data.text_content_length)

        file_txt = f"{base_name}.{test_data.ext_before}"

        link_response = disk_api.get_upload_link(file_txt, overwrite=False)
        assert link_response.status_code == HTTPStatus.OK, (
            f"Expected status {HTTPStatus.OK}, "
            f"actual {link_response.status_code}"
        )
        upload_link = UploadLink.model_validate(link_response.json())
        upload_response = disk_api.upload_to_link(
            upload_link.href, text_content)
        assert upload_response.status_code == HTTPStatus.CREATED, (
            f"Expected status {HTTPStatus.CREATED}, "
            f"actual {upload_response.status_code}"
        )

        logger.info("Step 4: verify file uploaded to disk with expected name")
        assert disk_page.is_file_present(file_txt), (
            f"Uploaded file not found on disk with name {file_txt}"
        )

        logger.info(
            "Step 5: open file in new tab and compare text with expected. Close new tab")
        disk_page.open_text_in_new_tab(file_txt)

        BrowserUtils.switch_to_last_tab()
        viewer = DocViewerPage()
        assert viewer.state.wait_for_displayed(), (
            f"{viewer.name} is not opened"
        )
        assert viewer.get_file_text() == text_content, "Actual text in file doesn't match expected"
        BrowserUtils.close_current_tab()

        logger.info("Step 6: use API to change file from txt to jpg")
        file_img = f"{base_name}.{test_data.ext_after}"
        move_response = disk_api.move(file_txt, file_img)
        assert move_response.status_code == HTTPStatus.CREATED, (
            f"Expected status {HTTPStatus.CREATED}, "
            f"actual {move_response.status_code}"
        )

        logger.info("Step 7: verify file extension changed")
        assert disk_page.is_file_absent(file_txt), (
            "Extension didn't change from txt"
        )
        assert disk_page.is_file_present(file_img), (
            "Extension didn't change to jpg"
        )

        logger.info(
            "Step 8: use API upload jpg with same file name from previous step")

        overwrite_link_response = disk_api.get_upload_link(
            file_img, overwrite=True)
        assert overwrite_link_response.status_code == HTTPStatus.OK, (
            f"Expected status {HTTPStatus.OK}, "
            f"actual {overwrite_link_response.status_code}"
        )
        overwrite_link = UploadLink.model_validate(
            overwrite_link_response.json())
        overwrite_response = disk_api.upload_to_link(
            overwrite_link.href,
            FileUtils.read_resource_bytes(test_data.img_file),
        )
        assert overwrite_response.status_code == HTTPStatus.CREATED, (
            f"Expected status {HTTPStatus.CREATED}, "
            f"actual {overwrite_response.status_code}"
        )

        logger.info(
            "Step 9: Open the image and verify that it matches the one uploaded. Close the image")
        disk_page.open_image_original(file_img)

        BrowserUtils.switch_to_last_tab()
        image_page = ImagePage()
        assert image_page.state.wait_for_displayed(), (
            f"{image_page.name} is not opened"
        )
        assert ImageUtils.matches_filename(image_page.get_img_src(), file_img), (
            "Opened image does not match uploaded file"
        )
        BrowserUtils.close_current_tab()

        logger.info("Step 10: drag image to trash")
        disk_page.drag_file_to_trash(file_img)
        assert disk_page.is_file_absent(file_img), "File didn't drag to trash"

        logger.info(
            "Step 11: use API to verify that the file from the previous step is in the trash")
        trash_response = disk_api.list_trash(sort=TrashSort.DELETED_DESC)
        assert trash_response.status_code == HTTPStatus.OK, (
            f"Expected status {HTTPStatus.OK}, "
            f"actual {trash_response.status_code}"
        )
        trash_body = TrashListResponse.model_validate(trash_response.json())
        trash_item = next(
            (item for item in trash_body.embedded.items if item.name == file_img),
            None,
        )

        assert trash_item is not None, "File not found in trash"

        trash_meta_response = disk_api.get_trash_resource(trash_item.path)
        assert trash_meta_response.status_code == HTTPStatus.OK, (
            f"Expected status {HTTPStatus.OK}, "
            f"actual {trash_meta_response.status_code}"
        )

        logger.info("Step 12: use API to restore file")
        restore_response = disk_api.restore(trash_item.path)
        assert restore_response.status_code == HTTPStatus.CREATED, (
            f"Expected status {HTTPStatus.CREATED}, "
            f"actual {restore_response.status_code}"
        )

        logger.info("Step 13: verify image is on the disk UI again")
        assert disk_page.is_file_present(file_img), (
            "Image not on the disk"
        )

        logger.info("Step 14: use API to delete image permanently from disk")
        delete_response = disk_api.delete_resource(file_img, permanently=True)

        assert delete_response.status_code == HTTPStatus.NO_CONTENT, (
            f"Expected status {HTTPStatus.NO_CONTENT}, "
            f"actual {delete_response.status_code}"
        )

        logger.info("Step 15: verify image deleted from disk UI")
        disk_page.sort_files()
        assert disk_page.is_file_absent(file_img), (
            "Image is on disk UI"
        )
