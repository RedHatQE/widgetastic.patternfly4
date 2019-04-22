import pytest
from widgetastic_patternfly4 import Pagination


@pytest.fixture
def paginator(browser):
    paginator = Pagination(browser, locator=".//div[@class='pf-c-pagination'][1]")
    yield paginator
    paginator.first_page()
    paginator.set_per_page(20)


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
        "100 per page"
    ]


@pytest.mark.parametrize("items_per_page", [10, 20, 50, 100])
def test_iteration(paginator, items_per_page):
    assert paginator.is_first_disabled
    paginator.set_per_page(items_per_page)
    expected_total_pages = 523 // items_per_page + 1
    assert paginator.is_previous_disabled
    for page in paginator:
        assert paginator.current_page == page
        assert paginator.total_pages == expected_total_pages
        if items_per_page * page > paginator.total_items:
            right_number = paginator.total_items
        else:
            right_number = items_per_page * page
        assert paginator.displayed_items == (1 + items_per_page * (page - 1), right_number)
        assert paginator.total_items == 523
    assert paginator.is_next_disabled
    assert paginator.is_last_disabled
