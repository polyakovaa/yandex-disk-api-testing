from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class MainPage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath(
                "//*[contains(@href,'disk.yandex.ru')]//*[text()='Войти']"),
            "Main page",
        )

    def click_login(self):
        self._element_factory.get_button(self.locator, "Login").click()
