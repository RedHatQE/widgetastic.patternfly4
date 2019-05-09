import pytest
from widgetastic.widget import View
from widgetastic_patternfly4 import Dropdown, DropdownItemDisabled, DropdownItemNotFound, Kebab


@pytest.fixture
def view(browser):
    class TestView(View):
        kebab = Kebab(
            ".//h4[@id='dropdown-with-kebab']/following::div"
            "/div[contains(@class, 'pf-c-dropdown')]"
        )
        dropdown_txt_locator = Dropdown("Dropdown")
        dropdown_custom_locator = Dropdown(
            locator=(
                ".//h4[@id='simple-dropdown']/following::div"
                "/div[contains(@class, 'pf-c-dropdown')]"
            )
        )
        dropdown_default_locator = Dropdown()

    return TestView(browser)


@pytest.fixture(
    params=[
        "dropdown_txt_locator", "dropdown_custom_locator", "dropdown_default_locator", "kebab"
    ]
)
def dropdown(view, request):
    return getattr(view, request.param)


def test_dropdown_is_displayed(dropdown):
    assert dropdown.is_displayed


def test_enabled_dropdown(dropdown):
    assert dropdown.is_enabled


def test_dropdown_items(dropdown):
    assert dropdown.items == ["Link", "Action", "Disabled Link", "Disabled Action",
                              "", "Separated Link", "Separated Action"]
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
