from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class DocViewerPage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath("//*[contains(@class,'doc-page')]"),
            "Text doc viewer page",
        )
        self.__page_text = self._element_factory.get_label(
            self.locator, "Page text"
        )

    def get_file_text(self) -> str:
        return self.__page_text.get_text()
