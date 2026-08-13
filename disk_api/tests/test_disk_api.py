from http import HTTPStatus
from pathlib import Path
import logging
from utils.random_utils import RandomUtils
from py_selenium_auto.browsers.browser_services import BrowserServices
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.disk_page import DiskPage
from steps.login_steps import LoginSteps
from pages.docviewer_page import DocViewerPage
from pages.image_page import ImagePage
from utils.image_utils import ImageUtils

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
        login_steps.fill_login_form(config.login, config.password)

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

        upload_response = disk_api.upload_file(
            file_txt, text_content, overwrite=False)

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

        BrowserServices.Instance.browser.tabs.switch_to_last_tab()
        viewer = DocViewerPage()
        assert viewer.state.wait_for_displayed(), (
            f"{viewer.name} is not opened"
        )
        assert viewer.get_file_text() == text_content, "Actual text in file doesn't match expected"
        BrowserServices.Instance.browser.tabs.close_tab()

        logger.info("Step 6: use API to change file from txt to jpg")
        file_img = f"{base_name}.{test_data.ext_after}"
        move_response = disk_api.move(file_txt, file_img)
        assert move_response.status_code == HTTPStatus.CREATED, (
            f"Expected status {HTTPStatus.CREATED}, "
            f"actual {move_response.status_code}"
        )

        logger.info("Step 7: verify file extention changed")
        assert disk_page.is_file_absent(file_txt), (
            "Extention didn't change from txt"
        )
        assert disk_page.is_file_present(file_img), (
            "Extention didn't change to jpg"
        )

        logger.info(
            "Step 8: use API upload jpg with same file name from previous step")

        with open(Path("resources") / test_data.img_file, "rb") as image:
            overwrite_response = disk_api.upload_file(
                file_img, image.read(), overwrite=True)
        assert overwrite_response.status_code == HTTPStatus.CREATED, (
            f"Expected status {HTTPStatus.CREATED}, "
            f"actual {overwrite_response.status_code}"
        )

        logger.info(
            "Step 9: Open the image and verify that it matches the one uploaded. Close the image")
        disk_page.open_image_original(file_img)
        image_page = ImagePage()
        assert image_page.state.wait_for_displayed(), (
            f"{image_page.name} is not opened"
        )
        assert ImageUtils.matches_filename(image_page.get_img_src(), file_img), (
            "Opened image does not match uploaded file"
        )
        image_page.close_img()

        logger.info("Step 10: drag image to trash")
        disk_page.drag_file_to_trash(file_img)
        assert disk_page.is_file_absent(file_img), "File didn't drag to trash"

        logger.info(
            "Step 11: use API to verify that the file from the previous step is in the trash")
        trash_item = disk_api.find_in_trash(
            file_img,
            page_size=test_data.trash_page_size,
            sort=test_data.trash_sort,
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

        logger.info("Step 13: verify image is on the disk again")
        assert disk_page.is_file_present(file_img), (
            "Image not on the disk"
        )

        logger.info("Step 14: use API to delete image permanently from disk")
        delete_response = disk_api.delete_resource(file_img, permanently=True)

        assert delete_response.status_code == HTTPStatus.NO_CONTENT, (
            f"Expected status {HTTPStatus.NO_CONTENT}, "
            f"actual {delete_response.status_code}"
        )

        logger.info("Step 15: verify image deleted from disk")
        assert disk_page.is_file_absent(file_img), (
            "Image was not deleted from the disk"
        )
