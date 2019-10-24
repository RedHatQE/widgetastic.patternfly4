from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import GenericLocatorWidget


class SwitchDisabled(Exception):
    pass


class Switch(GenericLocatorWidget):
    """Represents the Patternfly Switch.

    https://www.patternfly.org/v4/documentation/react/components/switch
    """

    CHECKBOX_LOCATOR = "./input"
    LABEL = (
        "./span[contains(@class, 'pf-m-on') and preceding-sibling::input[@checked] or "
        "contains(@class, 'pf-m-off') and preceding-sibling::input[not(@checked)]]"
    )

    @property
    def selected(self):
        """Returns a boolean detailing if the Switch is on (True) of off (False)."""
        return self.browser.get_attribute("checked", self.CHECKBOX_LOCATOR) is not None

    @property
    def label(self):
        """Returns the label of the Switch."""
        try:
            return self.browser.text(self.LABEL)
        except NoSuchElementException:
            return None

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
