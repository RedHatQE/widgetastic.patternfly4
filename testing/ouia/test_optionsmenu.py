import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import DropdownItemNotFound
from widgetastic_patternfly4.ouia import OptionsMenu

TESTING_PAGE_URL = (
    "https://patternfly-docs-ouia.netlify.app/documentation/react/components/optionsmenu"  # noqa
)


@pytest.fixture
def options_menu(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-optionsmenu-ouia']"
        options_menu = OptionsMenu("Simple Options Menu")

    return TestView(browser).options_menu


def test_options_menu_is_displayed(options_menu):
    assert options_menu.is_displayed


def test_enabled_options_menu(options_menu):
    assert options_menu.is_enabled


def test_options_menu_items(options_menu):
    assert options_menu.items == ["Option 1", "Option 2", "Option 3"]
    assert options_menu.has_item("Option 2")
    assert not options_menu.has_item("Non existing items")
    assert options_menu.item_enabled("Option 1")


def test_options_menu_open(options_menu):
    assert not options_menu.is_open
    options_menu.open()
    assert options_menu.is_open
    options_menu.close()
    assert not options_menu.is_open


def test_options_menu_item_select(options_menu):
    options_menu.item_select("Option 2")
    assert options_menu.selected_items[0] == "Option 2"
    assert not options_menu.is_open
    with pytest.raises(DropdownItemNotFound):
        options_menu.item_select("Non existing items")
