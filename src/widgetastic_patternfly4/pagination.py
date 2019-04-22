from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import GenericLocatorWidget, Text, TextInput, View, Widget

from . import Dropdown as VanillaDropdown


class Dropdown(VanillaDropdown):

    ROOT = ParametrizedLocator("{@locator}")
    BUTTON_LOCATOR = "./div/button"

    def __init__(self, parent, locator, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.locator = locator


class Pagination(View):
    """Represents the Patternfly pagination.

    http://patternfly-react.surge.sh/patternfly-4/components/pagination
    """

    ROOT = ParametrizedLocator("{@locator}")
    _first = GenericLocatorWidget(".//button[@data-action='first']")
    _previous = GenericLocatorWidget(".//button[@data-action='previous']")
    _next = GenericLocatorWidget(".//button[@data-action='next']")
    _last = GenericLocatorWidget(".//button[@data-action='last']")
    _options = Dropdown(".//div[contains(@class, 'pf-c-dropdown')]")
    _items = Text(".//span[@class='pf-c-options-menu__toggle-text']")
    _current_page = TextInput(locator=".//input[@aria-label='Current page']")
    _total_pages = Text(".//div[@class='pf-c-pagination__nav-page-select']/span")

    def __init__(self, parent, locator, logger=None):
        View.__init__(self, parent=parent, logger=logger)
        self.locator = locator

    @property
    def is_first_disabled(self):
        return "pf-m-disabled" in self.browser.classes(self._first)

    def first_page(self):
        self._first.click()

    @property
    def is_previous_disabled(self):
        return "pf-m-disabled" in self.browser.classes(self._previous)

    def previous_page(self):
        self._previous.click()

    @property
    def is_next_disabled(self):
        return "pf-m-disabled" in self.browser.classes(self._next)

    def next_page(self):
        self._next.click()

    @property
    def is_last_disabled(self):
        return "pf-m-disabled" in self.browser.classes(self._last)

    def last_page(self):
        self._last.click()

    @property
    def current_page(self):
        return int(self._current_page.value)

    @property
    def total_pages(self):
        # example "of 6 pages"
        return int(self._total_pages.text.strip().split()[1])

    @property
    def displayed_items(self):
        items_string = self._items.text
        # example "1 - 20 of 523 items"
        first_num, last_num = items_string.split("of")[0].split("-")
        return int(first_num.strip()), int(last_num.strip())

    @property
    def total_items(self):
        items_string = self._items.text
        return int(items_string.split("of")[1].split()[0])

    @property
    def per_page_options(self):
        return self._options.items

    def set_per_page(self, count):
        # support both digits (20 or "20") and exact string value ("20 per page")
        if not isinstance(count, str) or count.isdigit():
            value = '{} per page'.format(str(count))
        else:
            value = count
        if not self._options.has_item(value):
            raise ValueError(
                "count '{}' is not a valid option in the pagination dropdown".format(count)
            )

        self._options.item_select(value)

    def __iter__(self):
        self.first_page()
        self._page_counter = 0
        return self

    def __next__(self):
        if self._page_counter < self.total_pages:
            self._page_counter += 1
            if self._page_counter > 1:
                self.next_page()
            return self._page_counter
        else:
            raise StopIteration

    def next(self):
        # For sake Python 2 compatibility
        return self.__next__()
