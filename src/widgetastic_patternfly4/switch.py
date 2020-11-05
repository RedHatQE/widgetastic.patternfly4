from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import GenericLocatorWidget


class SwitchDisabled(Exception):
    pass


class BaseSwitch:
    """Represents the Patternfly Switch.

    https://www.patternfly.org/v4/documentation/react/components/switch
    """

    CHECKBOX_LOCATOR = "./input"
    LABEL_ON = "./span[contains(@class, 'pf-m-on')]"
    LABEL_OFF = "./span[contains(@class, 'pf-m-off')]"

    @property
    def selected(self):
        """Returns a boolean detailing if the Switch is on (True) of off (False)."""
        return self.browser.get_attribute("checked", self.CHECKBOX_LOCATOR) is not None

    def _read_locator(self, locator):
        try:
            return self.browser.text(locator)
        except NoSuchElementException:
            return None

    @property
    def label(self):
        """Returns the label of the Switch."""
        if self.selected:
            return self._read_locator(self.LABEL_ON)
        else:
            return self._read_locator(self.LABEL_OFF)

    @property
    def is_enabled(self):
        """Returns a boolean detailing if the switch is enabled."""
        return self.browser.get_attribute("disabled", self.CHECKBOX_LOCATOR) is None

    def fill(self, value):
        """Fills a Switch with the supplied value."""
        if not self.is_enabled:
            raise SwitchDisabled("{} is disabled".format(repr(self)))
        if bool(value) == self.selected:
            return False
        else:
            self.browser.click(self.CHECKBOX_LOCATOR)
            return True

    def read(self):
        """Returns a boolean detailing if the Switch is on (True) of off (False)."""
        return self.selected

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.locator)


class Switch(BaseSwitch, GenericLocatorWidget):
    pass
