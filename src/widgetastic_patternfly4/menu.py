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

    Most menu's exist without a toggle to open them (e.g. all the examples in the link below).
    That is why there is the class level constant IS_ALWAYS_OPEN which defaults to 'True'.

    However, it is possible to have a menu that will only appear based on a button or toggle.
    In these cases you should inherit from menu and set IS_ALWAYS_OPEN to 'False'. BUTTON_LOCATOR
    will also need to be modified to point to the toggle button. In the DOM, the menu widget is
    usually placed as a sibling to the toggle button. You can either override ROOT or simply pass
    a locator when the widget is instantiated to point to the parent of the toggle button.

    .. code-block:: python

        class PermissionsMenu(Menu):
            IS_ALWAYS_OPEN = False
            BUTTON_LOCATOR = ".//button[contains(@class, 'pf-c-menu-toggle')]"
            ROOT = f"{BUTTON_LOCATOR}/.."

    https://www.patternfly.org/v4/documentation/react/components/menu
    """

    # most menus are always open
    IS_ALWAYS_OPEN = True

    BUTTON_LOCATOR = "./button"
    ITEMS_LOCATOR = ".//li[contains(@class, 'pf-c-menu__list-item')]"
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
        """Returns True if the menu toggle itself is enabled and therefore interactive."""
        return self.IS_ALWAYS_OPEN or "disabled" not in self.browser.classes(self.BUTTON_LOCATOR)

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
        """Fills a Menu with a value or values."""
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


class BaseCheckboxMenu(BaseMenu):
    """
    Represents a checkbox menu.
    """

    ITEM_LOCATOR = ".//label[normalize-space(.)={}]/preceding-sibling::input"  # noqa

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
                    selected[item] = self.browser.element(
                        parent=el, locator="./input"
                    ).is_selected()
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


class CheckboxMenu(BaseCheckboxMenu, Dropdown):
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-menu")]'
