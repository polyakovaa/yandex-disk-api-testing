import pytest
from api.disk_api import DiskApi
from providers.config_provider import ConfigProvider
from providers.testdata_provider import ModelTestDataProvider
from utils.logger_utils import LoggerUtils
from py_selenium_auto.browsers.browser_services import BrowserServices
from providers.startup import Startup
from utils.file_utils import FileUtils
import os


def pytest_configure():
    LoggerUtils.setup()


@pytest.fixture
def disk_api(config):
    return DiskApi(
        base_url=config.base_url,
        timeout=config.timeout,
        oauth_token=config.oauth_token,
    )


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    BrowserServices.Instance.browser.maximize()
    yield
    if BrowserServices.Instance.is_browser_started:
        BrowserServices.Instance.browser.quit()


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    work_dir = str(FileUtils.find_project_root())
    os.chdir(work_dir)
    Startup.init_browser()
    yield


@pytest.fixture(scope="session")
def config():
    return ConfigProvider.get_instance()


@pytest.fixture(scope="session")
def test_data():
    return ModelTestDataProvider.get_instance()
