from collections import OrderedDict

from wait_for import wait_for
from widgetastic.exceptions import NoSuchElementException
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget
from widgetastic.xpath import quote


def check_nav_loaded(fn):
    def inner(self, *args, **kwargs):
        assert self.loaded
        return fn(self, *args, **kwargs)

    return inner


class BaseNavigation:
    """The Patternfly navigation.

    https://www.patternfly.org/v4/documentation/react/components/nav
    """

    CURRENTLY_SELECTED = (
        './/*[self::a or self::button][contains(@class, "pf-m-current") or '
        'parent::li[contains(@class, "pf-m-current")]]'
    )
    ITEMS = "./ul/li/*[self::a or self::button]"
    SUB_ITEMS_ROOT = "./section"
    ITEM_MATCHING = "./ul/li[.//*[self::a or self::button][normalize-space(.)={}]]"
    ITEM_MATCHING_OUIA = "./ul/li[@ouia-nav-group={text} or .//a[@ouia-nav-item={text}]]"

    @property
    def loaded(self):
        """Returns a boolean detailing if the nav is loaded."""
        out = self.browser.element(".").get_attribute("data-ouia-safe")
        if out == "false":
            self.logger.info("Navigation not ready yet")
            wait_for(
                lambda: self.browser.element(".").get_attribute("data-ouia-safe") == "true",
                num_sec=10,
            )
        elif not out:
            self.logger.info("Navigation doesn't have 'data-ouia-safe' property")
        return True

    @check_nav_loaded
    def read(self):
        """Returns the current navigation item."""
        return self.currently_selected

    @check_nav_loaded
    def nav_links(self, *levels):
        """Returns a list of all navigation items."""
        if not levels:
            return [el.get_property("textContent") for el in self.browser.elements(self.ITEMS)]
        current_item = self
        for i, level in enumerate(levels):
            li = self.browser.element(
                self.ITEM_MATCHING.format(quote(level.strip())), parent=current_item
            )

            try:
                current_item = self.browser.element(self.SUB_ITEMS_ROOT, parent=li)
            except NoSuchElementException:
                if i == len(levels) - 1:
                    return []
                else:
                    raise
        return [
            el.get_property("textContent")
            for el in self.browser.elements(self.ITEMS, parent=current_item)
        ]

    @check_nav_loaded
    def nav_item_tree(self, start=None):
        """Returns an ordered dict representing the navigation tree."""
        start = start or []
        result = OrderedDict()
        for item in self.nav_links(*start):
            sub_items = self.nav_item_tree(start=start + [item])
            result[item] = sub_items or None
        if result and all(value is None for value in result.values()):
            # If there are no child nodes, then just make it a list
            result = list(result.keys())
        return result

    @property
    @check_nav_loaded
    def currently_selected(self):
        """Returns the currently selected item."""
        return [self.browser.text(el) for el in self.browser.elements(self.CURRENTLY_SELECTED)]

    @check_nav_loaded
    def select(self, *levels, **kwargs):
        """Select an item in the navigation.

        Args:
            *levels: Items to be clicked in the navigation.
            force: Force navigation to happen, defaults to False.
        """
        self.logger.info("Selecting %r in navigation", levels)
        force = kwargs.get("force", False)
        if not force and list(levels) == self.currently_selected:
            return
        current_item = self
        for i, level in enumerate(levels, 1):
            try:
                li = self.browser.element(
                    self.ITEM_MATCHING.format(quote(level)), parent=current_item
                )
            except NoSuchElementException:
                li = self.browser.element(
                    self.ITEM_MATCHING_OUIA.format(text=quote(level)), parent=current_item
                )
            if "pf-m-expanded" not in li.get_attribute("class").split():
                self.browser.click(li)
            if i == len(levels):
                return
            current_item = self.browser.element(self.SUB_ITEMS_ROOT, parent=li)

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.ROOT)


class Navigation(BaseNavigation, Widget):
    ROOT = ParametrizedLocator("{@locator}")
    LOCATOR_START = './/nav[@class="pf-c-nav"{}]'

    def __init__(self, parent, label=None, id=None, locator=None, logger=None):
        super().__init__(parent, logger=logger)

        quoted_label = quote(label) if label else ""
        if label:
            label_part = " and @label={} or @aria-label={}".format(quoted_label, quoted_label)
        else:
            label_part = ""

        id_part = " and @id={}".format(quote(id)) if id else ""
        if locator is not None:
            self.locator = locator
        elif label_part or id_part:
            self.locator = self.LOCATOR_START.format(label_part + id_part)
        else:
            raise TypeError("You need to specify either, id, label or locator for Navigation")
