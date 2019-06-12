from collections import OrderedDict

from widgetastic.exceptions import NoSuchElementException
from widgetastic.utils import ParametrizedLocator
from widgetastic.xpath import quote
from widgetastic.widget import Widget
from wait_for import wait_for


def check_nav_loaded(fn):
    def inner(self, *args, **kwargs):
        assert self.loaded
        fn(self, *args, **kwargs)
    return inner

class Navigation(Widget):
    """The Patternfly navigation.

    https://pf-next.com/components/Nav/examples/
    """

    LOCATOR_START = '//nav[@class="pf-c-nav"{}]'
    ROOT = ParametrizedLocator("{@locator}")
    CURRENTLY_SELECTED = (
        './/a[contains(@class, "pf-m-current") or ' 'parent::li[contains(@class, "pf-m-current")]]'
    )
    ITEMS = "./ul/li/a"
    SUB_ITEMS_ROOT = "./section"
    ITEM_MATCHING = "./ul/li[.//a[normalize-space(.)={}]]"

    @property
    def loaded(self):
        if self._loaded:
            return True
        else:
            out = self.browser.element(self.ROOT).get_attribute('data-ouia-safe')
            if out == 'false':
                self.logger.info("Navigation not ready yet")
                wait_for(
                    lambda: self.browser.element(self.ROOT).get_attribute('data-ouia-safe')=='true',
                    num_sec=10
                )
            elif not out:
                self.logger.info("Navigation doesn't have 'data-ouia-safe' property")
            return True

    def __init__(self, parent, label=None, id=None, locator=None, logger=None):
        self._loaded = False
        Widget.__init__(self, parent, logger=logger)

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

    @check_nav_loaded
    def read(self):
        return self.currently_selected

    @check_nav_loaded
    def nav_links(self, *levels):
        import pdb;pdb.set_trace()
        if not levels:
            return [self.browser.text(el) for el in self.browser.elements(self.ITEMS)]
        current_item = self
        for i, level in enumerate(levels):
            li = self.browser.element(self.ITEM_MATCHING.format(quote(level)), parent=current_item)

            try:
                current_item = self.browser.element(self.SUB_ITEMS_ROOT, parent=li)
            except NoSuchElementException:
                if i == len(levels) - 1:
                    return []
                else:
                    raise

        return [
            self.browser.text(el) for el in self.browser.elements(self.ITEMS, parent=current_item)
        ]

    @check_nav_loaded
    def nav_item_tree(self, start=None):
        start = start or []
        result = OrderedDict()
        for item in self.nav_links(*start):
            sub_items = self.nav_item_tree(start=start + [item])
            result[item] = sub_items or None
        if result and all(value is None for value in result.values()):
            # If there are no child nodes, then just make it a list
            result = list(result.keys())
        return result

    @check_nav_loaded
    @property
    def currently_selected(self):
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
            li = self.browser.element(self.ITEM_MATCHING.format(quote(level)), parent=current_item)
            self.browser.click(li)
            if i == len(levels):
                return
            current_item = self.browser.element(self.SUB_ITEMS_ROOT, parent=li)

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.ROOT)
