from widgetastic.exceptions import NoSuchElementException

from .dropdown import Dropdown
from .dropdown import DropdownItemDisabled
from .dropdown import DropdownItemNotFound


class SelectItemDisabled(DropdownItemDisabled):
    pass


class SelectItemNotFound(DropdownItemNotFound):
    pass


class BaseSelect:
    """Represents the Patternfly Select.

    https://www.patternfly.org/v4/documentation/react/components/select
    """

    BUTTON_LOCATOR = "./button"
    ITEMS_LOCATOR = (
        ".//ul[@class='pf-c-select__menu']/li[contains(@class, 'pf-c-select__menu-wrapper')]"
    )
    ITEM_LOCATOR = ".//*[contains(@class, 'pf-c-select__menu-item') and normalize-space(.)={}]"
    SELECTED_ITEM_LOCATOR = (
        ".//span[contains(@class, 'ins-c-conditional-filter') and normalize-space(.)={}]"
    )
    TEXT_LOCATOR = (
        ".//div[contains(@class, 'pf-c-select') and child::button[normalize-space(.)={}]]"
    )

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


class Select(BaseSelect, Dropdown):
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-select")][1]'


class BaseCheckboxSelect(BaseSelect):
    """Represents the Patternfly Checkbox Select.

    https://www.patternfly.org/v4/documentation/react/components/select
    """

    ITEMS_LOCATOR = ".//label[contains(@class, 'pf-c-select__menu-item')]"
    ITEM_LOCATOR = f"{ITEMS_LOCATOR}/span[starts-with(normalize-space(.), {{}})]/preceding-sibling::input"  # noqa

    def item_select(self, items, close=True):
        """Opens the Checkbox and selects the desired item.

        Args:
            item: Item to be selected
            close: Close the dropdown when finished
        """
        if not isinstance(items, (list, tuple, set)):
            items = [items]

        try:
            for item in items:
                element = self.item_element(item, close=False)
                if not self.browser.is_selected(element):
                    element.click()
        finally:
            if close:
                self.close()

    def item_deselect(self, items, close=True):
        """Opens the Checkbox and deselects the desired item.

        Args:
            item: Item to be selected
            close: Close the dropdown when finished
        """
        if not isinstance(items, (list, tuple, set)):
            items = [items]

        try:
            for item in items:
                element = self.item_element(item, close=False)
                if self.browser.is_selected(element):
                    element.click()
        finally:
            if close:
                self.close()

    def fill(self, items):
        """Fills a Checkbox with all items.
        Example dictionary: {"foo": True, "bar": False, "baz": True}

        Args:
            items: A dictionary containing what items to select (True) or deselect (False)
        """
        try:
            for item, value in items.items():
                if value:
                    self.item_select(item, close=False)
                else:
                    self.item_deselect(item, close=False)
        finally:
            self.close()

    def read(self):
        """Returns a dictionary containing the selected status as bools."""
        selected = {}
        with self.opened():
            for el in self.browser.elements(self.ITEMS_LOCATOR):
                item = self.browser.text(el)
                try:
                    # get the child element of the label
                    selected[item] = el.find_element_by_xpath("./input").is_selected()
                except NoSuchElementException:
                    selected[item] = False

        return selected

    def _get_items(self, close=False):
        """Returns a list of all checkbox items as strings.

        Args:
            close: Close the dropdown when finished
        """
        self.open()
        result = [self.browser.text(el) for el in self.browser.elements(self.ITEMS_LOCATOR)]

        if close:
            self.close()

        return result

    @property
    def items(self):
        """Returns a list of all CheckboxSelect items as strings."""
        return self._get_items(close=True)


class CheckboxSelect(BaseCheckboxSelect, Dropdown):
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-select")][1]'
