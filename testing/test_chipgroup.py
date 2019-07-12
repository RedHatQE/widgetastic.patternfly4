import pytest
from widgetastic.widget import View
from widgetastic_patternfly4 import Chip, ChipGroup, ChipGroupToolbar, ChipReadOnlyError
from wait_for import wait_for


@pytest.fixture(scope="module")
def view(browser):
    _LOCATOR = ".//div[@class='pf-c-chip'][descendant::span[contains(., '{}')]]"

    class TestView(View):
        ROOT = ".//main[@role='main']"

        plain_chip = Chip(_LOCATOR.format("Chip 1"))
        long_chip = Chip(_LOCATOR.format("Really long Chip that goes on and on"))
        chip_with_badge = Chip(_LOCATOR.format("Chip7"))
        read_only_chip = Chip(
            ".//div[contains(@class, 'pf-c-chip') and contains(@class, 'pf-m-read-only')]"
        )

        chip_group_toolbar = ChipGroupToolbar()
        chip_group_multiselect = ChipGroup(
            locator=(
                ".//h2[(.)='Chip group multi-select']/"
                "following-sibling::div[1]/div/ul[contains(@class, 'pf-c-chip-group')]"
            )
        )
        badge_chip_group = ChipGroup(
            locator=(
                ".//h2[(.)='Badge chip group']/"
                "following-sibling::div[1]/div/ul[contains(@class, 'pf-c-chip-group')]"
            )
        )

    view = TestView(browser)

    wait_for(
        lambda: view.chip_group_multiselect.is_displayed,
        num_sec=3,
        delay=0.1,
        message="wait for chip-group-multi-select widget to appear on page",
    )

    return view


def test_chipgroup_chips(view):
    assert view.plain_chip.text == "Chip 1"
    assert not view.plain_chip.badge
    assert view.plain_chip.is_displayed
    assert not view.plain_chip.read_only
    assert view.plain_chip.read() == "Chip 1"
    view.plain_chip.remove()
    assert not view.plain_chip.is_displayed

    assert view.long_chip.text == "Really long Chip that goes on and on"
    assert not view.long_chip.badge
    assert view.long_chip.is_displayed
    assert not view.long_chip.read_only
    assert view.long_chip.read() == "Really long Chip that goes on and on"
    view.long_chip.remove()
    assert not view.long_chip.is_displayed

    assert view.chip_with_badge.text == "Chip"
    assert view.chip_with_badge.badge == "7"
    assert view.chip_with_badge.is_displayed
    assert not view.chip_with_badge.read_only
    assert view.chip_with_badge.read() == "Chip"
    view.chip_with_badge.remove()
    assert not view.chip_with_badge.is_displayed

    assert view.read_only_chip.text == "Read-only Chip"
    assert not view.read_only_chip.badge
    assert not view.read_only_chip.button.is_displayed
    assert view.read_only_chip.is_displayed
    assert view.read_only_chip.read_only
    assert view.read_only_chip.read() == "Read-only Chip"
    with pytest.raises(ChipReadOnlyError):
        view.read_only_chip.remove()


def test_chipgroup_multiselect(view):
    chip_group = view.chip_group_multiselect

    assert chip_group.is_displayed
    assert chip_group.label is None
    assert chip_group.multiselect
    chip_group.show_more()
    chip_group.show_less()

    expected_chips = ["Chip 1", "Really long chip that goes on and on", "Chip 3", "Chip 4"]
    chips = [chip.text for chip in chip_group]
    assert chips == expected_chips

    chip_group.show_less()
    expected_chips = ["Chip 1"]
    chips = [chip.text for chip in chip_group.get_chips(show_more=False)]
    assert chips == expected_chips

    chip_group.remove_chip_by_name("Chip 1")
    expected_chips = ["Really long chip that goes on and on", "Chip 3", "Chip 4"]
    assert chip_group.read() == expected_chips

    chip_group.remove_all_chips()
    assert not chip_group.is_displayed


def test_chipgroup_badge(view):
    chip_group = view.badge_chip_group

    assert chip_group.is_displayed
    assert chip_group.label is None
    assert chip_group.multiselect
    chip_group.show_more()
    chip_group.show_less()

    expected_chips = [("Lemons", "10"), ("Limes", "8")]
    chips = [(chip.text, chip.badge) for chip in chip_group]
    assert chips == expected_chips

    chip_group.show_less()
    expected_chips = [("Lemons", "10")]
    chips = [(chip.text, chip.badge) for chip in chip_group.get_chips(show_more=False)]
    assert chips == expected_chips

    chip_group.remove_chip_by_name("Lemons")
    expected_chips = ["Limes"]
    assert chip_group.read() == expected_chips

    chip_group.remove_all_chips()
    assert not chip_group.is_displayed


def test_chipgroup_toolbar(view):
    assert view.chip_group_toolbar.is_displayed

    groups = [group.label for group in view.chip_group_toolbar.get_groups()]
    assert groups == ["Category 1", "Category 2", "Category 3"]

    groups = [group.label for group in view.chip_group_toolbar]
    assert groups == ["Category 1", "Category 2", "Category 3"]

    data = {
        "Category 1": ["Chip 1", "Chip 2"],
        "Category 2": ["Chip 3", "Chip 4"],
        "Category 3": ["Chip 5", "Chip 6", "Chip 7", "Chip 8"],
    }
    assert view.chip_group_toolbar.read() == data

    view.chip_group_toolbar.show_less()
    data = {"Category 1": ["Chip 1", "Chip 2"]}
    groups = view.chip_group_toolbar.get_groups(show_more=False)
    assert len(groups) == 1
    assert groups[0].label == "Category 1"
    assert groups[0].read() == ["Chip 1", "Chip 2"]

    groups = view.chip_group_toolbar.get_groups()
    cat_2_group = [g for g in groups if g.label == "Category 2"][0]
    cat_2_group.remove_chip_by_name("Chip 3")
    data = {
        "Category 1": ["Chip 1", "Chip 2"],
        "Category 2": ["Chip 4"],
        "Category 3": ["Chip 5", "Chip 6", "Chip 7", "Chip 8"],
    }
    assert view.chip_group_toolbar.read() == data

    cat_2_group.remove_all_chips()
    data = {
        "Category 1": ["Chip 1", "Chip 2"],
        "Category 3": ["Chip 5", "Chip 6", "Chip 7", "Chip 8"],
    }
    assert view.chip_group_toolbar.read() == data

    for group in view.chip_group_toolbar:
        group.remove_all_chips()
    assert not view.chip_group_toolbar.is_displayed
