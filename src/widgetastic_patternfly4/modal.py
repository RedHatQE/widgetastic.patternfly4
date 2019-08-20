from widgetastic.exceptions import NoSuchElementException
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget
from widgetastic.xpath import quote


class ModalItemNotFound(Exception):
    pass


class Modal(Widget):
    """Represents the Patternfly Modal.

    https://www.patternfly.org/v4/documentation/react/components/modal
    """

    ROOT = ParametrizedLocator("{@locator}")
    BODY = ".//div[contains(@class, 'pf-c-modal-box__body')]"
    FOOTER = ".//div[contains(@class, 'pf-c-modal-box__footer')]/child::node()"
    FOOTER_ITEM = (
        ".//div[contains(@class, 'pf-c-modal-box__footer')]" "/button[normalize-space(.)={}]"
    )
    TITLE = ".//h1[contains(@class, 'pf-c-title')]"
    CLOSE = ".//button[@aria-label='Close']"

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator or ".//div[contains(@class, 'pf-c-modal-box')]"

    @property
    def title(self):
        """Get title of modal window."""
        return self.browser.text(self.browser.element(self.TITLE))

    @property
    def body(self):
        """Get WebElement of modal body."""
        return self.browser.element(self.BODY)

    def close(self):
        """Close modal window."""
        self.browser.click(self.browser.element(self.CLOSE))

    @property
    def footer_items(self):
        """Returns a list of strings of all items in modal footer."""
        return [self.browser.text(el) for el in self.browser.elements(self.FOOTER)]

    def footer_item(self, item):
        """Returns a WebElement for given item name in modal footer."""
        try:
            return self.browser.element(self.FOOTER_ITEM.format(quote(item)))
        except NoSuchElementException:
            raise ModalItemNotFound(f"Item {item} not found. Available items: {self.footer_items}")

    def __repr__(self):
        return f"{type(self).__name__}({self.locator!r})"
