from contextlib import contextmanager
import math

from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import GenericLocatorWidget, Text, TextInput, View

from .optionsmenu import OptionsMenu


class PaginationNavDisabled(Exception):
    pass


class Pagination(View):
    """Represents the Patternfly pagination.

    https://www.patternfly.org/v4/documentation/react/components/pagination
    """

    ROOT = ParametrizedLocator("{@locator}")
    DEFAULT_LOCATOR = (
        ".//div[contains(@class, 'pf-c-pagination') and not(contains(@class, 'pf-m-compact'))]"
    )

    _first = GenericLocatorWidget(".//button[contains(@data-action, 'first')]")
    _previous = GenericLocatorWidget(".//button[contains(@data-action, 'previous')]")
    _next = GenericLocatorWidget(".//button[contains(@data-action, 'next')]")
    _last = GenericLocatorWidget(".//button[contains(@data-action, 'last')]")
    _options = OptionsMenu()
    _items = Text(".//span[@class='pf-c-options-menu__toggle-text']")
    _current_page = TextInput(locator=".//input[@aria-label='Current page']")
    _total_pages = Text(".//div[@class='pf-c-pagination__nav-page-select']/span")

    def __init__(self, parent, locator=None, logger=None):
        View.__init__(self, parent=parent, logger=logger)
        if not locator:
            locator = self.DEFAULT_LOCATOR
        self.locator = locator
        self._cached_per_page_value = None

    @property
    def is_first_disabled(self):
        return not self.browser.element(self._first).is_enabled()

    def first_page(self):
        if self.is_first_disabled:
            raise PaginationNavDisabled("first")
        self._first.click()

    @property
    def is_previous_disabled(self):
        return not self.browser.element(self._previous).is_enabled()

    def previous_page(self):
        if self.is_previous_disabled:
            raise PaginationNavDisabled("previous")
        self._previous.click()

    @property
    def is_next_disabled(self):
        return not self.browser.element(self._next).is_enabled()

    def next_page(self):
        if self.is_next_disabled:
            raise PaginationNavDisabled("next")
        self._next.click()

    @property
    def is_last_disabled(self):
        return not self.browser.element(self._last).is_enabled()

    def last_page(self):
        if self.is_last_disabled:
            raise PaginationNavDisabled("last")
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

    @property
    def current_per_page(self):
        if self._cached_per_page_value:
            return self._cached_per_page_value
        return int(self._options.selected_items[0].split()[0])

    @contextmanager
    def cache_per_page_value(self):
        """
        A context manager that can be used to prevent looking up the 'current page' value.

        This adds some efficiencies when iterating over pages or in cases where it is safe to
        assume that the "per page" setting is not going to change and it's not necessary to
        re-read it from the browser repeatedly.
        """
        self._cached_per_page_value = None
        self._cached_per_page_value = self.current_per_page
        yield
        self._cached_per_page_value = None

    def set_per_page(self, count):
        # convert a possible int to string
        value = str(count)
        value_per_page = "{} per page".format(value)
        items = self._options.items
        if value_per_page in items:
            self._options.item_select(value_per_page)
        elif value in items:
            self._options.item_select(value)
        else:
            raise ValueError(
                "count '{}' is not a valid option in the pagination dropdown".format(count)
            )

    def __iter__(self):
        if self.current_page != 1:
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


class CompactPagination(Pagination):
    DEFAULT_LOCATOR = (
        ".//div[contains(@class, 'pf-c-pagination') and " "contains(@class, 'pf-m-compact')]"
    )

    @property
    def is_first_disabled(self):
        """Compact paginator has no 'first' button."""
        return self.is_previous_disabled

    def first_page(self):
        while not self.is_previous_disabled:
            self.previous_page()

    @property
    def is_last_disabled(self):
        """Compact paginator has no 'last' button."""
        return self.is_next_disabled

    def last_page(self):
        while not self.is_next_disabled:
            self.next_page()

    @property
    def current_page(self):
        """
        Calculate the current page we are on.

        Compact pagination does not explicitly show this, so use some math.

        For example, if "per page" is set to '20', we know that a page displaying
        items:
            1-20 is on 20/20 = page 1
            21-40 is on page 40/20 = page 2
            41-60 is on page 60/20 = page 3

        and so on.
        """
        _, last_num = self.displayed_items
        return math.ceil(last_num / self.current_per_page)

    @property
    def total_pages(self):
        """
        Calculate total page count.

        Compact pagination does not explicitily show the page count, so use some math.
        """
        return math.ceil(self.total_items / self.current_per_page)

    def __iter__(self):
        self.first_page()
        self._page_counter = 0
        return self

    def __next__(self):
        if not self.is_next_disabled:
            self._page_counter += 1
            if self._page_counter > 1:
                self.next_page()
            return self._page_counter
        else:
            raise StopIteration
