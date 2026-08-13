from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto.elements.label import Label
from selenium.webdriver import ActionChains
from py_selenium_auto.browsers.browser_services import BrowserServices


class DiskPage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath(
                "//a[contains(@href, 'disk') and contains(@class,'ServiceHeader')]"),
            "Disk page",
        )

        self.__open_more_button = self._element_factory.get_label(
            Locator.by_xpath(
                "//*[contains(@class , 'resources-action-bar')]//button[contains(@class , 'more-button')]"),
            "Open more")
        self.__view_file_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//*[contains(@class,'popup__action_type_view')]"),
            "View file")
        self.__open_img_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//*[contains(@class,'show-fullsize')]"),
            "Open img")
        self.__trash_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//*[contains(@id,'/trash')]"),
            "Trash")

    def _file_item(self, file_name: str) -> Label:
        return self._element_factory.get_label(
            Locator.by_xpath(
                f"//*[contains(@class,'listing-item__title') and contains(@aria-label, '{file_name}')]"
            ),
            f"File {file_name}",
        )

    def is_file_present(self, file_name: str) -> bool:
        item = self._file_item(file_name)
        if item.state.wait_for_exist():
            item.js_actions.scroll_into_view()
            return item.state.wait_for_displayed()
        return False

    def is_file_absent(self, file_name: str) -> bool:
        return self._file_item(file_name).state.wait_for_not_displayed()

    def open_text_in_new_tab(self, file_name: str):
        self._file_item(file_name).mouse_actions.right_click()
        self.__view_file_button.state.wait_for_displayed()
        self.__view_file_button.click()

    def open_image_original(self, file_name: str):
        self._file_item(file_name).mouse_actions.double_click()

    def drag_file_to_trash(self, file_name: str):
        file_item = self._file_item(file_name)
        file_item.state.wait_for_displayed()
        self.__trash_button.state.wait_for_displayed()
        driver = BrowserServices.Instance.browser.driver
        ActionChains(driver).click_and_hold(file_item.get_element()).pause(0.5).move_to_element(
            self.__trash_button.get_element()
        ).pause(0.5).release().perform()
