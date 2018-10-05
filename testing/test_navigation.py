import pytest
from widgetastic_patternfly4 import Navigation

from conftest import CustomBrowser

NAVS = [
    ("Primary Nav Default Example", ["Current link", "Link 2", "Link 3", "Link 4"],
        ["Current link"]),
    ("Primary Nav Expandable Example", {"Link 1 (current and expanded example)": ["Current link",
                                        "Subnav link 2", "Subnav link 3"],
                                        "Link 2 (expanded, but not current example)":
                                        ["Subnav link 1", "Subnav link 2"], "Link 3":
                                        ["Subnav link 1", "Subnav link 2"]},
        ["Link 1 (current and expanded example)", "Current link"]),
    ("Primary Nav Mixed Example", {"Link 1 (not expandable)": None,
                                   "Link 2 (expanded, but not current example)":
                                   ["Subnav link 1", "Subnav link 2"],
                                   "Link 4 (current, but not expanded example)":
                                   ["Subnav link 1", "Subnav link 2", "Subnav link 3"]},
        ["Link 4 (current, but not expanded example)", "Subnav link 2"])
]


@pytest.fixture(scope="module")
def browser(selenium):
    selenium.get("https://pf-next.com/components/nav/examples/")
    return CustomBrowser(selenium)


@pytest.mark.parametrize("sample", NAVS, ids=lambda sample: sample[0])
def test_navigation(browser, sample):
    label, tree, currently_selected = sample
    nav = Navigation(browser, label)
    assert nav.currently_selected == currently_selected
    assert nav.nav_item_tree() == tree
