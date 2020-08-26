import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import SelectItemNotFound
from widgetastic_patternfly4.ouia import SelectOUIA


class TestView(View):
    ROOT = ".//div[@id='ws-react-c-select-ouia']"
    select = SelectOUIA("Single")


@pytest.fixture
def select(browser):
    return TestView(browser).select


def test_select_is_displayed(select):
    assert select.is_displayed


def test_select_items(select):
    assert set(select.items) == {"Choose...", "Mr", "Miss", "Mrs", "Ms", "Dr", "Other"}
    assert select.has_item("Mr")
    assert not select.has_item("Non existing item")
    assert select.item_enabled("Miss")


def test_select_open(select):
    assert not select.is_open
    select.open()
    assert select.is_open
    select.close()
    assert not select.is_open


def test_select_item_select(select):
    select.fill("Mr")
    assert select.read() == "Mr"
    assert not select.is_open
    with pytest.raises(SelectItemNotFound):
        select.fill("Non existing item")
    assert not select.is_open
