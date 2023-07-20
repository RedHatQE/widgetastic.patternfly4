from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import GenericLocatorWidget
from widgetastic.widget import Text
from widgetastic.widget import TextInput

from widgetastic_patternfly4.button import Button


class BaseClipboardCopy:
    BUTTON_LOC = ".//button"
    TEXT_LOC = ".//input[contains(@class, 'pf-c-form-control')]"
    TEXT_LOC_INLINE = ".//span[contains(@class, 'pf-c-clipboard-copy__text')]"
    DEFAULT_LOCATOR = ".//div[contains(@class,'pf-c-clipboard-copy')]"

    text = TextInput(locator=TEXT_LOC)
    textInline = Text(locator=TEXT_LOC_INLINE)
    button = Button(locator=BUTTON_LOC)

    @property
    def is_editable(self):
        if self.is_inline:
            return False
        if self.browser.get_attribute("readonly", self.text):
            return False
        else:
            return True

    @property
    def is_inline(self):
        return "pf-m-inline" in self.browser.classes(self)

    def read(self):
        if self.is_inline:
            return self.textInline.text
        else:
            return self.text.value

    def fill(self, value):
        return self.text.fill(value)

    def copy(self):
        self.button.click()


class ClipboardCopy(BaseClipboardCopy, GenericLocatorWidget):
    ROOT = ParametrizedLocator("{@locator}")
