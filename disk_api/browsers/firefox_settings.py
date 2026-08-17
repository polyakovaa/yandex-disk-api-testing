from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from py_selenium_auto.configurations.web_driver_settings.driver_settings import DriverSettings
from enums.browser import BrowserName, BrowserPreference


class FirefoxSettings(DriverSettings):
    @property
    def browser_name(self) -> str:
        return BrowserName.FIREFOX

    @property
    def download_dir_capability_key(self) -> str:
        return BrowserPreference.FIREFOX_DOWNLOAD_DIR

    @property
    def driver_options(self) -> Options:
        options = Options()
        for name, value in (self._browser_options or {}).items():
            options.set_preference(name, value)
        for arg in self._browser_start_arguments or []:
            options.add_argument(arg)
        self._set_page_load_strategy(options)
        return options

    @property
    def driver_service(self) -> Service:
        return Service()
