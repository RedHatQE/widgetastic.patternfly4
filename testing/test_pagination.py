import contextlib

import pytest
from wait_for import wait_for
from widgetastic.widget import View

from widgetastic_patternfly4 import CompactPagination
from widgetastic_patternfly4 import Pagination
from widgetastic_patternfly4 import PaginationNavDisabled

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/pagination"


@contextlib.contextmanager
def _paginator(browser, request, reset_elements_per_page=True):
    paginator_cls, kind = request.param

    class TestView(View):
        ROOT = f".//div[@id='ws-react-c-pagination-{kind}']"
        paginator = paginator_cls(locator="./div")

    paginator = TestView(browser).paginator
    wait_for(lambda: paginator.is_displayed, num_sec=10)
    yield paginator
    try:
        paginator.first_page()
    except PaginationNavDisabled:
        # We are already at the first page...
        pass
    if reset_elements_per_page:
        paginator.set_per_page(20)


@pytest.fixture(
    params=[(Pagination, "top"), (CompactPagination, "compact")],
    ids=["Pagination", "CompactPagination"],
)
def paginator(browser, request):
    with _paginator(browser, request) as result:
        yield result


@pytest.fixture(
    params=[
        (Pagination, "one-page"),
        # there is no compact paginator of this type on the demo page
    ],
    ids=["Pagination"],
)
def one_page_paginator(browser, request):
    with _paginator(browser, request) as result:
        yield result


@pytest.fixture(
    params=[
        (Pagination, "no-items"),
        # there is no compact paginator of this type on the demo page
    ],
    ids=["Pagination"],
)
def no_elements_paginator(browser, request):
    with _paginator(browser, request, reset_elements_per_page=False) as result:
        yield result


# Can't parametrize fixtures:
# https://github.com/pytest-dev/pytest/issues/349
# @pytest.mark.parametrize('params', [ { "paginator": one_page_paginator, "expected_pages": 1}])


def _page_iteration_asserts(paginator, expected_pages):
    page_counter = 0

    with paginator.cache_per_page_value():
        for page in paginator:
            page_counter += 1
    assert page_counter == expected_pages


def test_one_page_iteration(one_page_paginator):
    _page_iteration_asserts(paginator=one_page_paginator, expected_pages=1)


def test_no_elements_iteration(no_elements_paginator):
    _page_iteration_asserts(paginator=no_elements_paginator, expected_pages=0)


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
    if isinstance(paginator, CompactPagination):
        pytest.skip("Cannot insert custom page number into CompactPagination")
    disp_items = paginator.displayed_items
    paginator.go_to_page(2)
    assert paginator.current_page == 2
    assert disp_items != paginator.displayed_items
