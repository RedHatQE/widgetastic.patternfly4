import calendar

import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import CalendarMonth

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/calendar-month"

MONTHS_LIST = list(calendar.month_name[1:])


@pytest.fixture
def calendar_month_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-calendar-month-selectable-date']"
        calendar = CalendarMonth(locator=".//div[@class='pf-c-calendar-month']")

    return TestView(browser)


def test_year_selection(calendar_month_view):
    assert calendar_month_view.calendar.year
    calendar_month_view.calendar.year = "2023"
    assert calendar_month_view.calendar.year == "2023"


def test_month_selection(calendar_month_view):
    assert calendar_month_view.calendar.month
    calendar_month_view.calendar.month = "December"
    assert calendar_month_view.calendar.month == "December"


def test_day_selection(calendar_month_view):
    calendar_month_view.calendar.day = "20"
    assert calendar_month_view.calendar.day == "20"
    calendar_month_view.calendar.next()
    assert not calendar_month_view.calendar.day


def _get_proper_month_index(index):
    max_index = len(MONTHS_LIST) - 1
    if index < 0:
        index = max_index
    elif index > max_index:
        index = 0

    return index


def test_month_navigation(calendar_month_view):
    current_month = calendar_month_view.calendar.month
    prev_month_index = _get_proper_month_index(MONTHS_LIST.index(current_month) - 1)
    next_month_index = _get_proper_month_index(MONTHS_LIST.index(current_month) + 1)

    calendar_month_view.calendar.prev()
    prev_month = calendar_month_view.calendar.month
    assert prev_month == MONTHS_LIST[prev_month_index]

    # reset to current default month
    calendar_month_view.calendar.month = current_month

    calendar_month_view.calendar.next()
    next_month = calendar_month_view.calendar.month
    assert next_month == MONTHS_LIST[next_month_index]


def test_fill_and_read(calendar_month_view):
    calendar_month_view.calendar.fill({"month": "February", "year": "2023"})
    result = calendar_month_view.calendar.read()
    assert result == " February 2023"

    with pytest.raises(TypeError):
        calendar_month_view.calendar.fill("foo")
