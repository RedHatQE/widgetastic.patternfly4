import pytest
from widgetastic.widget import ParametrizedView
from widgetastic.widget import View

from widgetastic_patternfly4 import CategoryChipGroup
from widgetastic_patternfly4 import Chip
from widgetastic_patternfly4 import ChipGroup
from widgetastic_patternfly4 import ChipReadOnlyError

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/chip-group"


@pytest.fixture(scope="module")
def chips_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-chip-group-single']"
        chips = ParametrizedView.nested(Chip)

    return TestView(browser)


@pytest.fixture(scope="module")
def chip_group_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-chip-group-simple-inline-chip-group']"

        non_existent_chip_group = ChipGroup(locator="foobar-locator")
        chip_group = ChipGroup()

    # Firefox fails the test if the chart is not fully visible therefore we click here on anchor
    # in order to properly scroll down
    anchor = browser.element("//a[@href='#simple-inline-chip-group']")
    browser.click(anchor)
    return TestView(browser)


@pytest.fixture(scope="module")
def category_chip_group_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-chip-group-chip-groups-with-categories-removable']"
        category_one = CategoryChipGroup(label="Category one")
        category_two = CategoryChipGroup(label="Category two has a very long name")

    return TestView(browser)


def test_non_existent_chips(chip_group_view):
    assert not chip_group_view.non_existent_chip_group.is_displayed


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


def test_chipgroup_simple(chip_group_view):
    assert chip_group_view.is_displayed
    assert chip_group_view.chip_group.is_displayed

    chips = [
        "Chip one",
        "Really long chip that goes on and on",
        "Chip three",
        "Chip four",
        "Chip five",
    ]
    assert chip_group_view.chip_group.read() == chips

    chip_group_view.chip_group.show_less()
    chips = ["Chip one", "Really long chip that goes on and on", "Chip three"]
    assert [chip.text for chip in chip_group_view.chip_group.get_chips(show_more=False)] == chips

    chips = ["Chip one", "Chip three", "Chip four", "Chip five"]
    chip_group_view.chip_group.remove_chip_by_name("Really long chip that goes on and on")
    assert chip_group_view.chip_group.read() == chips

    chip_group_view.chip_group.remove_all_chips()
    assert not chip_group_view.chip_group.has_chips


def test_chipgroup_category(category_chip_group_view):
    assert category_chip_group_view.category_one.is_displayed
    assert category_chip_group_view.category_one.label == "Category one"

    category_chip_group_view.category_one.close()
    assert not category_chip_group_view.category_one.is_displayed

    # This tests that a category disappears after all chips are removed
    category_chip_group_view.category_two.remove_all_chips()
    assert not category_chip_group_view.category_two.is_displayed
