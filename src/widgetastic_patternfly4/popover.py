from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget


class BasePopover:
    """Represents a popover.
    https://www.patternfly.org/v4/components/popover/

    For the popover to work, the base view should include a property
    popover = Popover()
    As there is supposed to only be one popover active at a time, this property
    should work, interacting with the active popover.
    """

    TITLE = """.//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6
                and contains(@class, "pf-c-title")]"""
    BODY = './/div[contains(@class, "pf-c-popover__body")]'
    FOOTER = ".//footer[contains(@class, 'pf-c-popover__footer')]"
    CLOSE = ".//button[@aria-label='Close']"

    def read(self):
        """Returns the text of the body of the popover as a string."""
        return self.body

    @property
    def _raw_title_el(self):
        return self.browser.element(self.TITLE)

    @property
    def _raw_description_el(self):
        return self.browser.element(self.BODY)

    @property
    def _raw_footer_el(self):
        return self.browser.element(self.TITLE)

    @property
    def title(self):
        """Returns the title text of the popover as a string."""
        return self.browser.text(self._raw_title_el)

    @property
    def body(self):
        """Returns the text of the body of the popover as a string."""
        el = self.browser.element(self.BODY)
        return self.browser.text(el)

    @property
    def footer(self):
        """Returns the text of the body of the popover as a string."""
        el = self.browser.element(self.FOOTER)
        return self.browser.text(el)

    def close(self):
        """Close popover window."""
        self.browser.click(self.browser.element(self.CLOSE))


class Popover(BasePopover, Widget):
    ROOT = ParametrizedLocator("{@locator}")
    DEFAULT_LOCATOR = ".//div[contains(@role, 'dialog') and contains(@class, 'pf-c-popover')]"

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        if locator:
            self.locator = locator
        else:
            self.locator = self.DEFAULT_LOCATOR
