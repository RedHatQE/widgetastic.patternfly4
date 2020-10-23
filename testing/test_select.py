import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import CheckboxSelect
from widgetastic_patternfly4 import Select
from widgetastic_patternfly4 import SelectItemNotFound

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/select"


@pytest.fixture
def select(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-select-single']"
        select = Select(locator=".//div[contains(@class, 'pf-c-select')]")

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


@pytest.fixture
def checkbox_select(browser):
    class TestView(View):
        ROOT = './/div[@id="ws-react-c-select-checkbox-input"]'
        checkbox_select = CheckboxSelect(locator=".//div[contains(@class, 'pf-c-select')]")

    return TestView(browser).checkbox_select


def test_checkbox_select_is_displayed(checkbox_select):
    assert checkbox_select.is_displayed


def test_checkbox_select_items(checkbox_select):
    assert set(checkbox_select.items) == {
        "Active This is a description",
        "Cancelled",
        "Paused",
        "Warning",
        "Restarted",
    }
    assert checkbox_select.has_item("Active This is a description")
    assert not checkbox_select.has_item("Non existing item")
    assert checkbox_select.item_enabled("Paused")


def test_checkbox_select_open(checkbox_select):
    assert not checkbox_select.is_open
    checkbox_select.open()
    assert checkbox_select.is_open
    checkbox_select.close()
    assert not checkbox_select.is_open


def test_checkbox_select_item_checkbox_select(checkbox_select):
    checkbox_select.fill({"Restarted": True, "Cancelled": True})
    assert checkbox_select.read() == {
        "Active This is a description": False,
        "Cancelled": True,
        "Paused": False,
        "Warning": False,
        "Restarted": True,
    }

    checkbox_select.fill(
        {"Cancelled": False, "Paused": False, "Warning": False, "Restarted": False}
    )

    assert checkbox_select.read() == {
        "Active This is a description": False,
        "Cancelled": False,
        "Paused": False,
        "Warning": False,
        "Restarted": False,
    }

    assert not checkbox_select.is_open
    with pytest.raises(SelectItemNotFound):
        checkbox_select.fill({"Non existing item": True})
    assert not checkbox_select.is_open
