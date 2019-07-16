import pytest
from widgetastic.widget import ParametrizedView, View
from widgetastic_patternfly4 import Chip, StandAloneChipGroup, ChipGroupToolbar, ChipReadOnlyError
from wait_for import wait_for


@pytest.fixture(scope="module")
def chips_view(browser):
    class TestView(View):
        ROOT = ".//main[@role='main']//h2[(.)='Chip']/following-sibling::div[1]/div"
        chips = ParametrizedView.nested(Chip)

    return TestView(browser)


@pytest.fixture(scope="module")
def root_view(browser):
    class TestView(View):
        ROOT = ".//main[@role='main']"

        chip_group_toolbar = ChipGroupToolbar()
        chip_group_multiselect = StandAloneChipGroup(
            locator=(
                ".//h2[(.)='Chip group multi-select']/"
                "following-sibling::div[1]/div/ul[contains(@class, 'pf-c-chip-group')]"
            )
        )
        badge_chip_group = StandAloneChipGroup(
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


def test_chipgroup_chips(chips_view):
    view = chips_view
    plain_chip = view.chips("Chip 1")
    long_chip = view.chips("Really long Chip that goes on and on")
    chip_with_badge = view.chips("Chip")
    read_only_chip = view.chips("Read-only Chip")

    assert plain_chip.text == "Chip 1"
    assert not plain_chip.badge
    assert plain_chip.is_displayed
    assert not plain_chip.read_only
    assert plain_chip.read() == "Chip 1"
    plain_chip.remove()
    assert not plain_chip.is_displayed

    assert long_chip.text == "Really long Chip that goes on and on"
    assert not long_chip.badge
    assert long_chip.is_displayed
    assert not long_chip.read_only
    assert long_chip.read() == "Really long Chip that goes on and on"
    long_chip.remove()
    assert not long_chip.is_displayed

    assert chip_with_badge.text == "Chip"
    assert chip_with_badge.badge == "7"
    assert chip_with_badge.is_displayed
    assert not chip_with_badge.read_only
    assert chip_with_badge.read() == "Chip"
    chip_with_badge.remove()
    assert not chip_with_badge.is_displayed

    assert read_only_chip.text == "Read-only Chip"
    assert not read_only_chip.badge
    assert not read_only_chip.button.is_displayed
    assert read_only_chip.is_displayed
    assert read_only_chip.read_only
    assert read_only_chip.read() == "Read-only Chip"
    with pytest.raises(ChipReadOnlyError):
        read_only_chip.remove()


def test_chipgroup_multiselect(root_view):
    view = root_view
    chip_group = view.chip_group_multiselect

    assert chip_group.is_displayed
    assert chip_group.label is None
    assert chip_group.is_multiselect
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


def test_chipgroup_badge(root_view):
    view = root_view
    chip_group = view.badge_chip_group

    assert chip_group.is_displayed
    assert chip_group.label is None
    assert chip_group.is_multiselect
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


def test_chipgroup_toolbar(root_view):
    view = root_view
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
