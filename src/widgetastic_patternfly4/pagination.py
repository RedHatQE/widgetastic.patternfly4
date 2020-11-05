import math
from contextlib import contextmanager

from selenium.webdriver.common.keys import Keys
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import GenericLocatorWidget
from widgetastic.widget import Text
from widgetastic.widget import TextInput
from widgetastic.widget import View

from .optionsmenu import OptionsMenu


class PaginationNavDisabled(Exception):
    pass


class BasePagination:
    """Represents the Patternfly pagination.

    https://www.patternfly.org/v4/documentation/react/components/pagination
    """

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

    @property
    def cached_per_page_value(self):
        return getattr(self, "_cached_per_page_value", None)

    @cached_per_page_value.setter
    def cached_per_page_value(self, value):
        self._cached_per_page_value = value

    @property
    def is_first_disabled(self):
        """Returns boolean detailing if the first page button is disabled."""
        return not self.browser.element(self._first).is_enabled()

    def first_page(self):
        """Clicks on the first page button."""
        if self.no_items or self.is_first_disabled:
            raise PaginationNavDisabled("first")
        self._first.click()

    @property
    def is_previous_disabled(self):
        """Returns boolean detailing if the previous page button is disabled."""
        return not self.browser.element(self._previous).is_enabled()

    def previous_page(self):
        """Clicks the previous page button."""
        if self.no_items or self.is_previous_disabled:
            raise PaginationNavDisabled("previous")
        self._previous.click()

    @property
    def is_next_disabled(self):
        """Returns boolean detailing if the next page button is disabled."""
        return not self.browser.element(self._next).is_enabled()

    def next_page(self):
        """Clicks the next page button."""
        if self.is_next_disabled:
            raise PaginationNavDisabled("next")
        self._next.click()

    @property
    def is_last_disabled(self):
        """Returns boolean detailing if the last page button is disabled."""
        return not self.browser.element(self._last).is_enabled()

    def last_page(self):
        """Clicks the last page button."""
        if self.is_last_disabled:
            raise PaginationNavDisabled("last")
        self._last.click()

    @property
    def current_page(self):
        """Returns an int of the current page number."""
        return int(self._current_page.value)

    @property
    def total_pages(self):
        """Returns int detailing the total number of pages."""
        return int(self._total_pages.text.strip().split()[1])

    @property
    def displayed_items(self):
        """Returns a string detailing the number of displayed items information.

        example "1 - 20 of 523 items"
        """
        items_string = self._items.text
        first_num, last_num = items_string.split("of")[0].split("-")
        return int(first_num.strip()), int(last_num.strip())

    @property
    def total_items(self):
        """Returns a string detailing the number of displayed items"""
        items_string = self._items.text
        return int(items_string.split("of")[1].split()[0])

    @property
    def per_page_options(self):
        """Returns an iterable of the available pagination options."""
        return self._options.items

    @property
    def no_items(self):
        """Returns wether the pagination object has elements or not"""
        return not self.total_items

    @property
    def current_per_page(self):
        """Returns an integer detailing how many items are shown per page."""
        if self.cached_per_page_value:
            return self.cached_per_page_value

        if self.no_items:
            return 0
        else:
            return int(self._options.selected_items[0].split()[0])

    @contextmanager
    def cache_per_page_value(self):
        """
        A context manager that can be used to prevent looking up the 'current page' value.

        This adds some efficiencies when iterating over pages or in cases where it is safe to
        assume that the "per page" setting is not going to change and it's not necessary to
        re-read it from the browser repeatedly.
        """
        self.cached_per_page_value = None
        self.cached_per_page_value = self.current_per_page
        yield
        self.cached_per_page_value = None

    def set_per_page(self, count):
        """Sets the number of items per page. (Will cast to str)"""
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

    def go_to_page(self, value):
        """Navigate to custom page number."""
        self._current_page.fill(value)
        self.browser.send_keys(Keys.RETURN, self._current_page)

    def __iter__(self):
        if self.current_page > 1:
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


class Pagination(BasePagination, View):
    ROOT = ParametrizedLocator("{@locator}")

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent=parent, logger=logger)
        if not locator:
            locator = self.DEFAULT_LOCATOR
        self.locator = locator


class BaseCompactPagination:
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
        """Compact paginator has no "last" button, so iterates until last is reached."""
        while not self.is_next_disabled:
            self.next_page()

    @property
    def current_page(self):
        """
        Calculate the current page we are on.

        Compact pagination does not explicitly show this, so use some math.

        For example, if "per page" is set to '20', we know that a page displaying items:
            1-20 is on 20/20 = page 1
            21-40 is on page 40/20 = page 2
            41-60 is on page 60/20 = page 3

        and so on.
        """
        if self.no_items:
            return 0
        else:
            _, last_num = self.displayed_items
            return math.ceil(last_num / self.current_per_page)

    @property
    def total_pages(self):
        """
        Calculate total page count.

        Compact pagination does not explicitily show the page count, so use some math.
        """
        if self.no_items:
            return 0
        else:
            return math.ceil(self.total_items / self.current_per_page)


class CompactPagination(BaseCompactPagination, Pagination):
    DEFAULT_LOCATOR = (
        ".//div[contains(@class, 'pf-c-pagination') and contains(@class, 'pf-m-compact')]"
    )
