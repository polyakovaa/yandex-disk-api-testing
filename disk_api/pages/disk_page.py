from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto.elements.label import Label
from selenium.webdriver import ActionChains
from py_selenium_auto.browsers.browser_services import BrowserServices
from selenium.webdriver.common.keys import Keys


class DiskPage(Form):
    _DRAG_OFFSET_X = 20
    _DRAG_OFFSET_Y = 20

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

        self.__delete_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//button[contains(@class,'confirmation-dialog__button_submit')]"),
            "Delete")

        self.__sort_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//*[contains(@class,'listing-sort')]"),
            "Sort")
        self.__size_sort_option = self._element_factory.get_button(
            Locator.by_xpath(
                "//*[@class='Menu-Group']//*[@value='size']"),
            "Size sort")

    def _file_item(self, file_name: str) -> Label:
        return self._element_factory.get_label(
            Locator.by_xpath(
                f"//*[contains(@class,'listing-item__title') and contains(@aria-label, '{file_name}')]"
            ),
            f"File {file_name}",
        )

    def _img_preview(self, file_name: str) -> Label:
        return self._element_factory.get_label(
            Locator.by_xpath(
                f"//*[contains(@class,'listing-item')]"
                f"[.//*[contains(@aria-label,'{file_name}') or contains(., '{file_name}')]]"
                f"//img"
            ),
            f"Preview {file_name}",
        )

    def is_file_present(self, file_name: str) -> bool:
        item = self._file_item(file_name)
        if item.state.wait_for_exist():
            item.js_actions.scroll_into_view()
            return item.state.wait_for_displayed()
        return False

    def is_file_absent(self, file_name: str) -> bool:
        return self._file_item(file_name).state.wait_for_not_exist()

    def open_text_in_new_tab(self, file_name: str):
        self._file_item(file_name).mouse_actions.right_click()
        self.__view_file_button.state.wait_for_displayed()
        self.__view_file_button.click()

    def open_image_original(self, file_name: str):
        self._file_item(file_name).click()
        self.__open_more_button.state.wait_for_displayed()
        self.__open_more_button.click()
        self.__open_img_button.state.wait_for_displayed()
        self.__open_img_button.click()

    def drag_file_to_trash(self, file_name: str):
        self.reset_selection()
        preview = self._img_preview(file_name)
        preview.js_actions.scroll_into_view()
        preview.state.wait_for_displayed()
        self.__trash_button.state.wait_for_displayed()

        source = preview.get_element()
        target = self.__trash_button.get_element()
        driver = BrowserServices.Instance.browser.driver
        ActionChains(driver).click_and_hold(source).move_by_offset(
            self._DRAG_OFFSET_X, self._DRAG_OFFSET_Y
        ).move_to_element(target).release().perform()

        if self.__delete_button.state.wait_for_displayed():
            self.__delete_button.click()

    def reset_selection(self):
        BrowserServices.Instance.browser.driver.switch_to.active_element.send_keys(
            Keys.ESCAPE)

    def sort_files(self):
        self.__sort_button.js_actions.scroll_into_view()
        self.__sort_button.click()
        self.__size_sort_option.click()
