from http import HTTPStatus
from pathlib import Path
import logging
from utils.random_utils import RandomUtils

logger = logging.getLogger(__name__)


class TestDiskApi:
    def test_disk_api(self, test_data, disk_api):
        logger.info("Step 3: use API to upload text file with random text")
        base_name = RandomUtils.generate_string_field(
            test_data.text_content_length)

        text_content = RandomUtils.generate_string_field(
            test_data.text_content_length)

        file_before = f"{base_name}.{test_data.ext_before}"
        file_after = f"{base_name}.{test_data.ext_after}"
        file_after_name = Path(file_after).name

        upload_response = disk_api.upload_file(
            file_before, text_content, overwrite=False)
        assert upload_response.status_code == HTTPStatus.CREATED

        logger.info("Step 6: use API to change file from txt to jpg")
        move_response = disk_api.move(file_before, file_after)
        assert move_response.status_code == HTTPStatus.CREATED

        logger.info(
            "Step 8: use API upload jpg with same file name from previous step")
        with open(Path("resources") / test_data.img_file, "rb") as image:
            overwrite_response = disk_api.upload_file(
                file_after, image.read(), overwrite=True)
        assert overwrite_response.status_code == HTTPStatus.CREATED

        delete_response = disk_api.delete_resource(
            file_after, permanently=False)
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

        logger.info(
            "Step 11: use API to verify that the file from the previous step is in the trash")
        trash_item = disk_api.find_in_trash(
            file_after_name,
            page_size=test_data.trash_page_size,
            sort=test_data.trash_sort,
        )
        assert trash_item is not None
        assert trash_item.name == file_after_name

        trash_meta_response = disk_api.get_trash_resource(trash_item.path)
        assert trash_meta_response.status_code == HTTPStatus.OK

        logger.info("Step 12: use API to restore file")
        restore_response = disk_api.restore(trash_item.path)
        assert restore_response.status_code in (
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
        )
        logger.info("Step 14: use API to delete file permanently from disk")
        delete_response = disk_api.delete_resource(
            file_after, permanently=True)
        assert delete_response.status_code == HTTPStatus.NO_CONTENT
