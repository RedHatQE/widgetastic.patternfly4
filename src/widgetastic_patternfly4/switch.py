from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import GenericLocatorWidget


class SwitchDisabled(Exception):
    pass


class Switch(GenericLocatorWidget):
    """Represents the Patternfly Switch.

    http://patternfly-react.surge.sh/patternfly-4/components/switch
    """

    CHECKBOX_LOCATOR = "./input"
    LABEL = './span[contains(@class, "pf-c-switch__label")]'

    @property
    def selected(self):
        return self.browser.get_attribute("checked", self.CHECKBOX_LOCATOR) is not None

    @property
    def label(self):
        try:
            return self.browser.text(self.LABEL)
        except NoSuchElementException:
            return None

    @property
    def is_enabled(self):
        return self.browser.get_attribute("disabled", self.CHECKBOX_LOCATOR) is None

    def fill(self, value):
        if not self.is_enabled:
            raise SwitchDisabled("{} is disabled".format(repr(self)))
        if bool(value) == self.selected:
            return False
        else:
            self.browser.click(self.CHECKBOX_LOCATOR)
            return True

    def read(self):
        return self.selected

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.locator)
