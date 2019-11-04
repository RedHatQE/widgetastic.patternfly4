from contextlib import contextmanager

from widgetastic.exceptions import NoSuchElementException
from widgetastic.xpath import quote

from .dropdown import Dropdown, DropdownItemNotFound, DropdownItemDisabled


class SelectItemDisabled(DropdownItemDisabled):
    pass


class SelectItemNotFound(DropdownItemNotFound):
    pass


class Select(Dropdown):
    """Represents the Patternfly Select.

    https://www.patternfly.org/v4/documentation/react/components/select
    """

    BUTTON_LOCATOR = "./button"
    ITEMS_LOCATOR = ".//ul[@class='pf-c-select__menu']/li"
    ITEM_LOCATOR = (
        ".//button[contains(@class, 'pf-c-select__menu-item')" " and normalize-space(.)={}]"
    )
    TEXT_LOCATOR = (
        './/div[contains(@class, "pf-c-select") and ' "child::button[normalize-space(.)={}]]"
    )
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-select")][1]'

    def item_element(self, item, close=True):
        """Returns a WebElement for given item name."""
        try:
            return super().item_element(item, close)
        except DropdownItemNotFound:
            raise SelectItemNotFound(
                "Item {!r} not found in {}. Available items: {}".format(
                    item, repr(self), self.items
                )
            )

    def item_select(self, item):
        """Opens the Select and selects the desired item.

        Args:
            item: Item to be selected

        Raises:
            SelectItemDisabled: if item is disabled
        """
        try:
            return super().item_select(item)
        except DropdownItemDisabled:
            raise SelectItemDisabled(
                'Item "{}" of {} is disabled\n'
                "The following items are available and enabled: {}".format(
                    item, repr(self), self.enabled_items
                )
            )

    def fill(self, value):
        """Fills a Select with a value."""
        self.item_select(value)

    def read(self):
        """Returns a string of the text of the selected option."""
        return self.browser.text(self.BUTTON_LOCATOR)


class CheckboxSelect(Select):
    ITEMS_LOCATOR = ".//label[contains(@class, 'pf-c-select__menu-item')]"
    ITEM_LOCATOR = (
        f"{ITEMS_LOCATOR}/span[starts-with(normalize-space(.), {{}})]/preceding-sibling::input"
    )

    def item_select(self, items):
        if not hasattr(items, '__iter__'):
            items = [items]
        try:
            for item in items:
                element = self.item_element(item, close=False)
                if not self.browser.is_selected(element):
                    element.click()
        finally:
            self.close()

    def item_deselect(self, items):
        pass    

    def fill(self, value):
        """
        {"item1": True, "item2": False}
        """
        pass

    def read(self):
        """
        Returns {"item1": True, "item2": False}
        """
        pass
    
