import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import DropdownItemNotFound
from widgetastic_patternfly4 import OptionsMenu

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/options-menu"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-options-menu-single-option']"
        options_menu_txt_locator = OptionsMenu("Options menu")
        options_menu_custom_locator = OptionsMenu(
            locator=".//div[contains(@class, 'pf-c-options-menu')]"
        )
        options_menu_default_locator = OptionsMenu()

    return TestView(browser)


@pytest.fixture(
    params=[
        "options_menu_txt_locator",
        "options_menu_custom_locator",
        "options_menu_default_locator",
    ]
)
def options_menu(view, request):
    return getattr(view, request.param)


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
