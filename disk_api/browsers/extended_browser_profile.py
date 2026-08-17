from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.configurations.web_driver_settings.chrome_settings import ChromeSettings
from py_selenium_auto.configurations.web_driver_settings.driver_settings import DriverSettings
from browsers.firefox_settings import FirefoxSettings
from enums.browser import BrowserName


class ExtendedBrowserProfile(BrowserProfile):
    def __init__(self, settings_file):
        super().__init__(settings_file)
        self._settings_file = settings_file

    @property
    def driver_settings(self) -> DriverSettings:
        if self.browser_name.lower() == BrowserName.FIREFOX:
            return FirefoxSettings(self._settings_file)
        if self.browser_name.lower() == BrowserName.CHROME:
            return ChromeSettings(self._settings_file)
        raise ValueError(
            f"No DriverSettings for browser {self.browser_name}"
        )
