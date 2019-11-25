import pytest

from widgetastic_patternfly4 import CompactPagination
from widgetastic_patternfly4 import Pagination
from widgetastic_patternfly4 import PaginationNavDisabled


@pytest.fixture(
    params=[
        (Pagination, {"locator": "(.//div[@id='pagination-options-menu-top'])[1]"}),
        (CompactPagination, {}),
    ],
    ids=["Pagination", "CompactPagination"],
)
def paginator(browser, request):
    paginator_cls, kwargs = request.param
    paginator = paginator_cls(browser, **kwargs)
    yield paginator
    try:
        paginator.first_page()
    except PaginationNavDisabled:
        # We are already at the first page...
        pass
    paginator.set_per_page(20)


@pytest.fixture(
    params=[
        (Pagination, {"locator": "(.//div[@id='pagination-options-menu-top'])[4]"}),
        (CompactPagination, {"locator": "(.//div[@id='pagination-options-menu-top'])[4]"}),
    ],
    ids=["Pagination", "CompactPagination"],
)
def one_page_paginator(browser, request):
    paginator_cls, kwargs = request.param
    paginator = paginator_cls(browser, **kwargs)
    yield paginator
    try:
        paginator.first_page()
    except PaginationNavDisabled:
        # We are already at the first page...
        pass
    paginator.set_per_page(20)


def test_one_page_iteration(one_page_paginator):

    page_counter = 0

    with one_page_paginator.cache_per_page_value():
        for page in one_page_paginator:
            page_counter += 1
    assert page_counter


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
