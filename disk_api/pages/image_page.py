from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from enums.element_attribute import ElementAttribute


class ImagePage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath("//img[@src]"),
            "Image page",
        )
        self.__image = self._element_factory.get_label(self.locator, "Image")

    def get_img_src(self) -> str:
        return self.__image.get_attribute(ElementAttribute.SRC)
