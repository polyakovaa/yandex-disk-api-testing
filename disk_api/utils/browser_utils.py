from py_selenium_auto.browsers.browser_services import BrowserServices


class BrowserUtils:
    __START_URL = "startUrl"

    @staticmethod
    def go_to_start_url():
        settings = BrowserServices.Instance.service_provider.settings_file()
        BrowserServices.Instance.browser.go_to(
            settings.get(BrowserUtils.__START_URL))

    @staticmethod
    def switch_to_last_tab():
        BrowserServices.Instance.browser.tabs.switch_to_last_tab()

    @staticmethod
    def close_current_tab():
        BrowserServices.Instance.browser.tabs.close_tab()
