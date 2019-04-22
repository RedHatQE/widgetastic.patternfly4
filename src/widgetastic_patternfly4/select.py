from contextlib import contextmanager

from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import GenericLocatorWidget
from widgetastic.xpath import quote


class SelectItemDisabled(Exception):
    pass


class SelectItemNotFound(Exception):
    pass


class Select(GenericLocatorWidget):
    """Represents the Patternfly Select.

    http://patternfly-react.surge.sh/patternfly-4/components/select
    """

    BUTTON_LOCATOR = "./button"
    ITEMS_LOCATOR = ".//ul[@class='pf-c-select__menu']/li"
    ITEM_LOCATOR = (
        ".//button[contains(@class, 'pf-c-select__menu-item')" " and normalize-space(.)={}]"
    )

    @contextmanager
    def opened(self):
        self.open()
        yield
        self.close()

    @property
    def is_open(self):
        return "pf-m-expanded" in self.browser.classes(self)

    def open(self):
        if not self.is_open:
            self.browser.click(self.BUTTON_LOCATOR)

    def close(self):
        if self.is_open:
            self.browser.click(self)

    @property
    def items(self):
        """Returns a list of all Select items as strings."""
        with self.opened():
            result = [self.browser.text(el) for el in self.browser.elements(self.ITEMS_LOCATOR)]
        return result

    @property
    def enabled_items(self):
        """Returns a list of all enabled Select items as strings."""
        result = []
        with self.opened():
            for el in self.browser.elements(self.ITEMS_LOCATOR):
                item_value = self.browser.text(el)
                if self.item_enabled(item_value):
                    result.append(item_value)
        return result

    def has_item(self, item):
        """Returns whether the items exists.

        Args:
            item: item name

        Returns:
            Boolean - True if enabled, False if not.
        """
        return item in self.items

    def item_element(self, item, close=True):
        """Returns a WebElement for given item name."""
        try:
            self.open()
            result = self.browser.element(self.ITEM_LOCATOR.format(quote(item)))
            if close:
                self.close()
            return result
        except NoSuchElementException:
            raise SelectItemNotFound(
                "Item {!r} not found in {}. Available items: {}".format(
                    item, repr(self), self.items
                )
            )

    def item_enabled(self, item, close=True):
        """Returns whether the given item is enabled.

        Args:
            item: Name of the item or item WebElement.

        Returns:
            Boolean - True if enabled, False if not.
        """
        el = self.item_element(item, close=False)
        is_el_enabled = "pf-m-disabled" not in self.browser.classes(el)
        if close:
            self.close()
        return is_el_enabled

    def item_select(self, item):
        """Opens the Select and selects the desired item.

        Args:
            item: Item to be selected

        Raises:
            SelectItemDisabled: if item is disabled
        """
        self.logger.info("Selecting %r in %r", item, self)
        with self.opened():
            if not self.item_enabled(item, close=False):
                raise SelectItemDisabled(
                    'Item "{}" of {} is disabled\n'
                    "The following items are available and enabled: {}".format(
                        item, repr(self), self.enabled_items
                    )
                )
            self.browser.click(self.item_element(item, close=False))

    def fill(self, value):
        self.item_select(value)

    def read(self):
        return self.browser.text(self.BUTTON_LOCATOR)

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.locator)
