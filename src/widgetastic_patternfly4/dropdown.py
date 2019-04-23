from contextlib import contextmanager

from widgetastic.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from widgetastic.utils import ParametrizedLocator
from widgetastic.xpath import quote
from widgetastic.widget import Widget


class DropdownDisabled(Exception):
    pass


class DropdownItemDisabled(Exception):
    pass


class DropdownItemNotFound(Exception):
    pass


class Dropdown(Widget):
    """Represents the Patternfly dropdown.

    http://patternfly-react.surge.sh/patternfly-4/components/dropdown

    Args:
        text: Text of the button, can be the inner text or the title attribute.

    """

    ROOT = ParametrizedLocator(
        './/div[contains(@class, "pf-c-dropdown") and '
        "child::button[normalize-space(.)={@text|quote}]]"
    )
    BUTTON_LOCATOR = "./button"
    ITEMS_LOCATOR = ".//ul[@class='pf-c-dropdown__menu']/li"
    ITEM_LOCATOR = (
        ".//*[self::a or self::button][contains(@class, 'pf-c-dropdown__menu-item')"
        " and normalize-space(.)={}]"
    )

    def __init__(self, parent, text, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.text = text

    @contextmanager
    def opened(self):
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
        return "pf-m-expanded" in self.browser.classes(self)

    def open(self):
        self._verify_enabled()
        if not self.is_open:
            self.browser.click(self.BUTTON_LOCATOR)

    def close(self, ignore_nonpresent=False):
        """Close the dropdown

        Args:
            ignore_nonpresent: Will ignore exceptions due to disabled or missing dropdown
        """
        try:
            self._verify_enabled()
            if self.is_open:
                self.browser.click(self)
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

    def item_element(self, item, close=True):
        """Returns a WebElement for given item name."""
        try:
            self.open()
            result = self.browser.element(self.ITEM_LOCATOR.format(quote(item)))
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

    def item_enabled(self, item, close=True):
        """Returns whether the given item is enabled.

        Args:
            item: Name of the item.

        Returns:
            Boolean - True if enabled, False if not.
        """
        self._verify_enabled()
        el = self.item_element(item, close=False)
        is_el_enabled = "pf-m-disabled" not in self.browser.classes(el)
        if close:
            self.close()
        return is_el_enabled

    def item_select(self, item, handle_alert=None):
        """Opens the dropdown and selects the desired item.

        Args:
            item: Item to be selected
            handle_alert: How to handle alerts. None - no handling, True - confirm, False - dismiss.

        Raises:
            DropdownItemDisabled
        """
        self.logger.info("Selecting %r", item)
        try:
            if not self.item_enabled(item, close=False):
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
                self.item_element(item, close=False), ignore_ajax=handle_alert is not None
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

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, getattr(self, "text", None) or self.locator)


class Kebab(Dropdown):
    """The so-called "kebab" widget of Patternfly."""

    ROOT = ParametrizedLocator("{@locator}")

    def __init__(self, parent, locator, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.locator = locator
