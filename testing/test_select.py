import pytest
from widgetastic.widget import View
from widgetastic_patternfly4 import Select, SelectItemNotFound


@pytest.fixture
def view(browser):
    class TestView(View):
        select = Select(locator='.//div[contains(@class, "pf-c-select")]')

    return TestView(browser)


def test_select_is_displayed(view):
    assert view.select.is_displayed


def test_select_items(view):
    assert set(view.select.items) == {'Choose...', 'Mr', 'Miss', 'Mrs', 'Ms', 'Dr', 'Other'}
    assert view.select.has_item('Mr')
    assert not view.select.has_item('Non existing item')
    assert view.select.item_enabled('Miss')


def test_select_open(view):
    assert not view.select.is_open
    view.select.open()
    assert view.select.is_open
    view.select.close()
    assert not view.select.is_open


def test_select_item_select(view):
    view.select.fill('Mr')
    assert view.select.read() == 'Mr'
    assert not view.select.is_open
    with pytest.raises(SelectItemNotFound):
        view.select.fill('Non existing item')
    assert not view.select.is_open
