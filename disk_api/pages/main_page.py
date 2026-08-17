from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class MainPage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath(
                "//a[.//*[text()='Войти']]"),
            "Main page",
        )

    def __get_login_button(self):
        return self._element_factory.get_button(self.locator, "Login")

    def click_login(self):
        login_button = self.__get_login_button()
        login_button.click()
