import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import DropdownItemDisabled
from widgetastic_patternfly4 import DropdownItemNotFound
from widgetastic_patternfly4.ouia import Dropdown

TESTING_PAGE_URL = (
    "https://patternfly-docs-ouia.netlify.app/documentation/react/components/dropdown"  # noqa
)


@pytest.fixture
def dropdown(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-dropdown-ouia']"
        dropdown = Dropdown("Dropdown")

    view = TestView(browser)
    return view.dropdown


def test_dropdown_is_displayed(dropdown):
    assert dropdown.is_displayed


def test_enabled_dropdown(dropdown):
    assert dropdown.is_enabled


def test_dropdown_items(dropdown):
    assert dropdown.items == [
        "Link",
        "Action",
        "Disabled Link",
        "Disabled Action",
        "",
        "Separated Link",
        "Separated Action",
    ]
    assert dropdown.has_item("Action")
    assert not dropdown.has_item("Non existing items")
    assert dropdown.item_enabled("Action")
    assert not dropdown.item_enabled("Disabled Link")


def test_dropdown_open(dropdown):
    assert not dropdown.is_open
    dropdown.open()
    assert dropdown.is_open
    dropdown.close()
    assert not dropdown.is_open


def test_dropdown_item_select(dropdown):
    dropdown.item_select("Action")
    assert not dropdown.is_open
    with pytest.raises(DropdownItemDisabled):
        dropdown.item_select("Disabled Link")
    with pytest.raises(DropdownItemNotFound):
        dropdown.item_select("Non existing items")
