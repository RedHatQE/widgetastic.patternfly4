from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget


class BaseDescriptionList:
    """Represents the Patternfly Description list.

    https://www.patternfly.org/v4/components/description-list
    """

    TERM_LOCATOR = ".//dt"
    DESC_LOCATOR = ".//dd"

    def read(self):
        """Return a dictionary of term / description pairs."""
        terms = [self.browser.text(el) for el in self.browser.elements(self.TERM_LOCATOR)]
        descs = [self.browser.text(el) for el in self.browser.elements(self.DESC_LOCATOR)]
        return dict(zip(terms, descs))


class DescriptionList(BaseDescriptionList, Widget):
    ROOT = ParametrizedLocator("{@locator}")
    DEFAULT_LOCATOR = ".//dl[contains(@class, 'pf-c-description-list')]"

    def __init__(self, parent, locator=None, logger=None):
        """Initialize the widget with the given locator."""
        super().__init__(parent, logger=logger)
        self.locator = locator or self.DEFAULT_LOCATOR
