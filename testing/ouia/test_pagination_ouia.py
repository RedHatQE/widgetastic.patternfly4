import pytest
from wait_for import wait_for
from widgetastic.widget import View

from widgetastic_patternfly4 import PaginationNavDisabled
from widgetastic_patternfly4.ouia import Pagination

TESTING_PAGE_URL = (
    "https://patternfly-docs-ouia.netlify.app/documentation/react/components/pagination"  # noqa
)


@pytest.fixture
def paginator(browser, request):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-pagination-ouia']"
        paginator = Pagination("pagination-options-menu-top")

    paginator = TestView(browser).paginator
    wait_for(lambda: paginator.is_displayed, num_sec=10)
    yield paginator
    try:
        paginator.first_page()
    except PaginationNavDisabled:
        # We are already at the first page...
        pass


def test_first_page(paginator):
    paginator.last_page()
    assert paginator.current_page == 27
    paginator.first_page()
    assert paginator.is_first_disabled
    assert paginator.is_previous_disabled
    assert not paginator.is_next_disabled
    assert not paginator.is_last_disabled
    assert paginator.current_page == 1
    assert paginator.total_pages == 27
    assert paginator.displayed_items == (1, 20)
    assert paginator.total_items == 523


def test_previous_page(paginator):
    paginator.next_page()
    assert paginator.current_page == 2
    paginator.previous_page()
    assert not paginator.is_next_disabled
    assert not paginator.is_last_disabled
    assert paginator.current_page == 1
    assert paginator.total_pages == 27
    assert paginator.displayed_items == (1, 20)
    assert paginator.total_items == 523


def test_next_page(paginator):
    paginator.next_page()
    assert not paginator.is_first_disabled
    assert not paginator.is_previous_disabled
    assert not paginator.is_next_disabled
    assert not paginator.is_last_disabled
    assert paginator.current_page == 2
    assert paginator.total_pages == 27
    assert paginator.displayed_items == (21, 40)
    assert paginator.total_items == 523


def test_last_page(paginator):
    paginator.last_page()
    assert not paginator.is_first_disabled
    assert not paginator.is_previous_disabled
    assert paginator.is_next_disabled
    assert paginator.is_last_disabled
    assert paginator.current_page == 27
    assert paginator.total_pages == 27
    assert paginator.displayed_items == (521, 523)
    assert paginator.total_items == 523


def test_per_page_options(paginator):
    assert paginator.per_page_options == [
        "10 per page",
        "20 per page",
        "50 per page",
        "100 per page",
    ]


@pytest.mark.parametrize("items_per_page", [50, 100])
def test_iteration(paginator, items_per_page):
    assert paginator.is_first_disabled
    paginator.set_per_page(items_per_page)
    assert paginator.current_per_page == items_per_page

    # Ensure we're always using an int for the math calculations
    items_per_page_int = int(str(items_per_page).split()[0])

    expected_total_pages = 523 // items_per_page_int + 1
    assert paginator.is_previous_disabled
    with paginator.cache_per_page_value():
        for page in paginator:
            assert paginator.current_page == page
            assert paginator.total_pages == expected_total_pages
            if items_per_page_int * page > paginator.total_items:
                right_number = paginator.total_items
            else:
                right_number = items_per_page_int * page
            assert paginator.displayed_items == (1 + items_per_page_int * (page - 1), right_number)
            assert paginator.total_items == 523
    assert paginator.is_next_disabled
    assert paginator.is_last_disabled


def test_bad_paginator_page_value(paginator):
    with pytest.raises(ValueError):
        paginator.set_per_page(9999999)
    with pytest.raises(ValueError):
        paginator.set_per_page("999999")


def test_custom_page(paginator):
    disp_items = paginator.displayed_items
    paginator.go_to_page(2)
    assert paginator.current_page == 2
    assert disp_items != paginator.displayed_items
