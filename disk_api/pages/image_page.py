from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator
from pages.element_attribute import ElementAttribute


class ImagePage(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath(
                "//img[contains(@class,'scalable-preview__image')]"),
            "Image page",
        )
        self.__image = self._element_factory.get_label(
            Locator.by_xpath(
                "//img[contains(@class,'scalable-preview__image')]"),
            "Image",
        )
        self.__close_button = self._element_factory.get_button(
            Locator.by_xpath(
                "//button[contains(@class,'slider__button_close')]"),
            "Close img",
        )

    def get_img_src(self) -> str:
        return self.__image.get_attribute(ElementAttribute.SRC)

    def close_img(self):
        self.__close_button.click()
