from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class LoginPage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath(
                "//*[contains(@class, 'body-auth')]"),
            "Login page",
        )
        self.__email_input = self._element_factory.get_text_box(
            Locator.by_xpath(
                "//input[contains(@data-testid, 'text-field-input')]"),
            "Email")

        self.__password_input = self._element_factory.get_text_box(
            Locator.by_xpath(
                "//input[contains(@type, 'password')]"),
            "Password")

        self.__next_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//button[contains(@data-testid, 'next')]"),
            "Next")
        self.__remind_later_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//button[contains(@data-testid, 'later')]"),
            "Remind later")

    def fill_email(self, email: str):
        self.__email_input.clear_and_type(email)

    def fill_password(self, password: str):
        self.__password_input.clear_and_type(password)

    def click_next(self):
        self.__next_button.click()

    def click_remind_later(self):
        self.__remind_later_button.click()
