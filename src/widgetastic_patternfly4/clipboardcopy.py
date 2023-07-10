from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import TextInput
from widgetastic.widget import View

from widgetastic_patternfly4.button import Button


class BaseClipboardCopy:
    BUTTON_LOC = ".//button[contains(@class, 'pf-c-button pf-m-control')]"
    TEXT_LOC = ".//input[contains(@class, 'pf-c-form-control')]"

    @property
    def is_editable(self):
        if self.browser.get_attribute("readonly", self.text):
            return False
        else:
            return True

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        if locator:
            self.locator = locator
        else:
            self.locator = self.DEFAULT_LOCATOR


class ClipboardCopy(BaseClipboardCopy, View):
    ROOT = ParametrizedLocator("{@locator}")
    DEFAULT_LOCATOR = ".//div[contains(@class,'pf-c-clipboard-copy')]"

    text = TextInput(locator=BaseClipboardCopy.TEXT_LOC)
    button = Button(locator=BaseClipboardCopy.BUTTON_LOC)

    def read(self):
        return self.text.value

    def fill(self, value):
        return self.text.fill(value)

    def copy(self):
        self.button.click()
