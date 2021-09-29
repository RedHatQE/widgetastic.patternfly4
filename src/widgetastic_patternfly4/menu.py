from widgetastic.exceptions import NoSuchElementException

from .dropdown import Dropdown
from .dropdown import DropdownItemDisabled
from .dropdown import DropdownItemNotFound


class MenuItemDisabled(DropdownItemDisabled):
    pass


class MenuItemNotFound(DropdownItemNotFound):
    pass


class BaseMenu:
    """Represents the Patternfly Menu.

    https://www.patternfly.org/v4/documentation/react/components/menu
    """

    # most menus are always open
    IS_ALWAYS_OPEN = True

    BUTTON_LOCATOR = "./button"
    ITEMS_LOCATOR = ".//ul[@class='pf-c-menu__list']/li[contains(@class, 'pf-c-menu__list-item')]"
    SELECTED_ITEMS_LOCATOR = ".//button[contains(@class, 'pf-m-selected')]"
    ITEM_LOCATOR = ".//*[contains(@class, 'pf-c-menu__list-item') and normalize-space(.)={}]"
    TEXT_LOCATOR = ".//div[contains(@class, 'pf-c-menu') and child::button[normalize-space(.)={}]]"

    @property
    def selected_items(self):
        """Returns a list of all selected items as strings."""
        with self.opened():
            result = [
                self.browser.text(el) for el in self.browser.elements(self.SELECTED_ITEMS_LOCATOR)
            ]
        return result

    @property
    def is_open(self):
        """
        Returns True if the Dropdown is open

        Some menus are visible without having to click anything, so if the items are displayed
        we consider that to be open as well.
        """
        return self.IS_ALWAYS_OPEN or "pf-m-expanded" in self.browser.classes(self.BUTTON_LOCATOR)

    @property
    def is_enabled(self):
        """Returns if the dropdown itself is enabled and therefore interactive."""
        return "disabled" not in self.browser.classes(self.ROOT)

    def close(self, ignore_nonpresent=False):
        """Close the menu

        It it is always open we do nothing

        Args:
            ignore_nonpresent: Will ignore exceptions due to disabled or missing dropdown
        """
        try:
            self._verify_enabled()
            if self.IS_ALWAYS_OPEN:
                self.logger.info("Tried to close %r but it's always open. Ignoring.", self)
                return
            if self.is_open:
                self.browser.click(self.BUTTON_LOCATOR)
        except (NoSuchElementException, MenuItemDisabled):
            if ignore_nonpresent:
                self.logger.info("%r hid so it was not possible to close it. But ignoring.", self)
            else:
                raise

    def item_element(self, item, close=True):
        """Returns a WebElement for given item name."""
        try:
            return super().item_element(item, close)
        except DropdownItemNotFound:
            raise MenuItemNotFound(
                "Item {!r} not found in {}. Available items: {}".format(
                    item, repr(self), self.items
                )
            )

    def item_select(self, item):
        """Opens the Menu and selects the desired item.

        Args:
            item: Item to be selected

        Raises:
            MenuItemDisabled: if item is disabled
        """
        try:
            return super().item_select(item)
        except DropdownItemDisabled:
            raise MenuItemDisabled(
                'Item "{}" of {} is disabled\n'
                "The following items are available and enabled: {}".format(
                    item, repr(self), self.enabled_items
                )
            )

    def fill(self, value):
        """Fills a Menu with a value."""
        if isinstance(value, list):
            for val in value:
                self.item_select(val)
        else:
            self.item_select(value)

    def read(self):
        """Returns a string of the text of the selected option."""
        if self.selected_items:
            return self.browser.text(self.SELECTED_ITEMS_LOCATOR)
        else:
            return self.browser.text(self)


class Menu(BaseMenu, Dropdown):
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-menu")]'
