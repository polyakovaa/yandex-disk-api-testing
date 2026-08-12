import pytest
from api.disk_api import DiskApi
from providers.config_provider import ConfigProvider
from providers.testdata_provider import ModelTestDataProvider
from utils.logger_utils import LoggerUtils


def pytest_configure():
    LoggerUtils.setup()


@pytest.fixture
def disk_api():
    config = ConfigProvider.get_instance()
    return DiskApi(
        base_url=config.base_url,
        timeout=config.timeout,
        oauth_token=config.oauth_token,
    )


@pytest.fixture(scope="session")
def test_data():
    return ModelTestDataProvider.get_instance()
