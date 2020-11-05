from contextlib import contextmanager

from wait_for import wait_for_decorator
from widgetastic.exceptions import NoSuchElementException
from widgetastic.exceptions import UnexpectedAlertPresentException
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Checkbox
from widgetastic.widget import Widget
from widgetastic.xpath import quote


class DropdownDisabled(Exception):
    pass


class DropdownItemDisabled(Exception):
    pass


class DropdownItemNotFound(Exception):
    pass


class BaseDropdown:
    """Represents the Patternfly dropdown.

    https://www.patternfly.org/v4/documentation/react/components/dropdown

    Args:
        text: Text of the button, can be the inner text or the title attribute.

    """

    BUTTON_LOCATOR = ".//button[contains(@class, 'pf-c-dropdown__toggle')]"
    ITEMS_LOCATOR = ".//ul[contains(@class, 'pf-c-dropdown__menu')]/li"
    ITEM_LOCATOR = ".//*[contains(@class, 'pf-c-dropdown__menu-item') and normalize-space(.)={}]"

    @contextmanager
    def opened(self):
        """A context manager to open and then close a Dropdown."""
        self.open()
        yield
        self.close()

    @property
    def is_enabled(self):
        """Returns if the dropdown itself is enabled and therefore interactive."""
        return "disabled" not in self.browser.classes(self.BUTTON_LOCATOR)

    def _verify_enabled(self):
        if not self.is_enabled:
            raise DropdownDisabled(
                '{} "{}" is not enabled'.format(
                    type(self).__name__, getattr(self, "text", self.locator)
                )
            )

    @property
    def is_open(self):
        """Returns True if the Dropdown is open"""
        return "pf-m-expanded" in self.browser.classes(self)

    def open(self):
        """Opens a dropdown."""
        self._verify_enabled()
        if self.is_open:
            return

        @wait_for_decorator(timeout=3)
        def _click():
            self.browser.click(self.BUTTON_LOCATOR)
            return self.is_open

    def close(self, ignore_nonpresent=False):
        """Close the dropdown

        Args:
            ignore_nonpresent: Will ignore exceptions due to disabled or missing dropdown
        """
        try:
            self._verify_enabled()
            if self.is_open:
                self.browser.click(self.BUTTON_LOCATOR)
        except (NoSuchElementException, DropdownDisabled):
            if ignore_nonpresent:
                self.logger.info("%r hid so it was not possible to close it. But ignoring.", self)
            else:
                raise

    @property
    def items(self):
        """Returns a list of all dropdown items as strings."""
        with self.opened():
            result = [self.browser.text(el) for el in self.browser.elements(self.ITEMS_LOCATOR)]
        return result

    def has_item(self, item):
        """Returns whether the items exists.

        Args:
            item: item name

        Returns:
            Boolean - True if enabled, False if not.
        """
        return item in self.items

    def item_element(self, item, close=True, **kwargs):
        """Returns a WebElement for given item name."""
        try:
            self.open()
            result = self.browser.element(self.ITEM_LOCATOR.format(quote(item)), **kwargs)
            if close:
                self.close()
            return result
        except NoSuchElementException:
            try:
                items = self.items
            except NoSuchElementException:
                items = []
            if items:
                items_string = "These items are present: {}".format("; ".join(items))
            else:
                items_string = "The dropdown is probably not present"
            raise DropdownItemNotFound("Item {!r} not found. {}".format(item, items_string))

    def item_enabled(self, item, close=True, **kwargs):
        """Returns whether the given item is enabled.

        Args:
            item: Name of the item.

        Returns:
            Boolean - True if enabled, False if not.
        """
        self._verify_enabled()
        el = self.item_element(item, close=False, **kwargs)
        is_el_enabled = "pf-m-disabled" not in self.browser.classes(el)
        if close:
            self.close()
        return is_el_enabled

    def item_select(self, item, handle_alert=None, **kwargs):
        """Opens the dropdown and selects the desired item.

        Args:
            item: Item to be selected
            handle_alert: How to handle alerts. None - no handling, True - confirm, False - dismiss.

        Raises:
            DropdownItemDisabled
        """
        self.logger.info("Selecting %r", item)
        try:
            if not self.item_enabled(item, close=False, **kwargs):
                raise DropdownItemDisabled(
                    'Item "{}" of {} "{}" is disabled\n'
                    "The following items are available: {}".format(
                        item,
                        type(self).__name__.lower(),
                        getattr(self, "text", None) or self.locator,
                        ";".join(self.items),
                    )
                )
            self.browser.click(
                self.item_element(item, close=False, **kwargs), ignore_ajax=handle_alert is not None
            )
            if handle_alert is not None:
                self.browser.handle_alert(cancel=not handle_alert, wait=10.0)
                self.browser.plugin.ensure_page_safe()
        finally:
            try:
                self.close(ignore_nonpresent=True)
            except UnexpectedAlertPresentException:
                self.logger.warning("There is an unexpected alert present.")
                pass

    @property
    def button_text(self):
        """Returns a string of the current dropdown name."""
        return self.browser.text(self.BUTTON_LOCATOR)

    def read(self):
        return self.button_text

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, getattr(self, "text", None) or self.locator)


class Dropdown(BaseDropdown, Widget):
    ROOT = ParametrizedLocator("{@locator}")
    TEXT_LOCATOR = (
        ".//div[contains(@class, 'pf-c-dropdown') and child::button[normalize-space(.)={}]]"
    )
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-dropdown")][1]'

    def __init__(self, parent, text=None, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        if locator and text:
            raise ValueError("Either text or locator should be provided")
        if text:
            self.locator = self.TEXT_LOCATOR.format(quote(text))
        elif locator:
            self.locator = locator
        else:
            self.locator = self.DEFAULT_LOCATOR


class BaseGroupDropdown:
    """Dropdown with grouped items in it."""

    ITEMS_LOCATOR = ".//section[@class='pf-c-dropdown__group']/ul/li"
    GROUPS_LOCATOR = ".//section[@class='pf-c-dropdown__group']/h1"
    GROUP_LOCATOR = ".//section[@class='pf-c-dropdown__group'][h1[normalize-space(.)={}]]"

    @property
    def groups(self):
        """Returns a list of all group names as strings."""
        with self.opened():
            result = [self.browser.text(el) for el in self.browser.elements(self.GROUPS_LOCATOR)]
        return result

    def item_element(self, item, group_name=None, close=True):
        """Returns a WebElement for given item name."""
        self.open()
        try:
            kwargs = (
                {"parent": self.browser.element(self.GROUP_LOCATOR.format(quote(group_name)))}
                if group_name
                else {}
            )
        except NoSuchElementException:
            raise DropdownItemNotFound(
                'Following group "{}" not found. Available are: {}'.format(group_name, self.groups)
            )
        return super().item_element(item, close=close, **kwargs)

    def item_select(self, item, group_name=None, handle_alert=None):
        """Opens the dropdown and selects the desired item. Implemented only for proper kwargs
        suggestions.

        Args:
            item: Item to be selected
            group_name: name of a group to search in. If not provided - all groups will be checked.
            handle_alert: How to handle alerts. None - no handling, True - confirm, False - dismiss.

        Raises:
            DropdownItemDisabled
        """
        return super().item_select(item, handle_alert=handle_alert, group_name=group_name)


class GroupDropdown(BaseGroupDropdown, Dropdown):
    pass


class BaseSplitButtonDropdown:
    """Represents the Patternfly Split Button Dropdown.

    https://www.patternfly.org/v4/documentation/react/components/dropdown#split-button-with-text
    """

    toggle_check = Checkbox(locator=".//input[@type='checkbox']")

    def check(self):
        """Check toggle checkbox."""
        return self.toggle_check.fill(True)

    def uncheck(self):
        """Uncheck toggle checkbox."""
        return self.toggle_check.fill(False)

    @property
    def selected(self):
        """Returns selected or not"""
        return self.toggle_check.selected

    def read(self):
        return self.browser.text(self)


class SplitButtonDropdown(BaseSplitButtonDropdown, Dropdown):
    pass
