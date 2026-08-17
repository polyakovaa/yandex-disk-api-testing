from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from py_selenium_auto.browsers.browser_factory.local_browser_factory import LocalBrowserFactory
from enums.browser import BrowserName


class ExtendedLocalBrowserFactory(LocalBrowserFactory):
    @property
    def _driver(self) -> WebDriver:
        if self._browser_profile.browser_name.lower() != BrowserName.FIREFOX:
            return super()._driver
        settings = self._browser_profile.driver_settings
        self._web_driver = FirefoxWebDriver(options=settings.driver_options)
        return self._web_driver
