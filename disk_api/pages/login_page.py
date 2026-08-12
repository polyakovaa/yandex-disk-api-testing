from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class LoginPage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath(
                "//*[contains(@class, 'body-auth')]"),
            "Login page",
        )
        self.__login_input = self._element_factory.get_text_box(
            Locator.by_xpath(
                "//input[contains(@data-testid, 'text-field-input')]"),
            "Login")

        self.__next_button - self._element_factory.get_button(
            Locator.by_xpath(
                "//button[contains(@data-testid, 'add-user-next')]"),
            "Next")

    def fill_login(self, login: str):
        self.__login_input.clear_and_type(login)

    def click_next(self):
        self.__next_button.click()
