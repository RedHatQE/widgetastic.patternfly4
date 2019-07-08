import pytest
from widgetastic.widget import View
from widgetastic_patternfly4 import (
    Dropdown,
    DropdownItemDisabled,
    DropdownItemNotFound,
    GroupDropdown,
)


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//h2[normalize-space(.)='Simple dropdown']/following-sibling::div[1]"
        dropdown_txt_locator = Dropdown("Dropdown")
        dropdown_custom_locator = Dropdown(locator=".//div[contains(@class, 'pf-c-dropdown')]")
        dropdown_default_locator = Dropdown()
        group_dropdown = GroupDropdown(
            locator=(
                "//h2[normalize-space(.)='Dropdown with groups']/following-sibling::div[1]"
                "//div[contains(@class, 'pf-c-dropdown')]"
            )
        )

    return TestView(browser)


@pytest.fixture(
    params=[
        "dropdown_txt_locator", "dropdown_custom_locator", "dropdown_default_locator"
    ]
)
def dropdown(view, request):
    return getattr(view, request.param)


@pytest.fixture()
def group_dropdown(view):
    return view.group_dropdown


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


def test_group_dropdown(group_dropdown):
    assert group_dropdown.is_displayed
    assert group_dropdown.is_enabled
    assert group_dropdown.items == [
        "Link", "Action", "Group 2 Link", "Group 2 Action", "Group 3 Link", "Group 3 Action"]
    assert group_dropdown.has_item("Group 2 Link")
    assert group_dropdown.item_enabled("Group 3 Action")
    assert group_dropdown.groups == ["Group 2", "Group 3"]
    group_dropdown.item_select("Link")
    group_dropdown.item_select("Group 3 Link", group_name="Group 3")
    with pytest.raises(DropdownItemNotFound):
        group_dropdown.item_select("Group 3 Link", group_name="Group 2")
