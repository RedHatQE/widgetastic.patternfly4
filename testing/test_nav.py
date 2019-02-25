import pytest
from widgetastic_patternfly4 import Navigation


NAVS = [
    (".//nav[@id='nav-primary-simple']", ["Link 1", "Link 2", "Link 3 with separator", "Link 4"],
        ["Link 1"]),
    (".//h1[normalize-space(.)='Expandable Nav']/following-sibling::section//nav", {
        "Link 1":
        ["Subnav Link 1", "Subnav Link 2 with separator",
         "Subnav Link 3"],
        "Link 2":
        ["Custom onClick", "Subnav Link 1", "Subnav Link 2",
         "Subnav Link 3"]
    },
        ["Link 1", "Subnav Link 1"]),
    (".//h1[normalize-space(.)='Nav Mixed']/following-sibling::section//nav", {
        "Link 1 (not expandable)": None,
        "Link 2 - expandable":
        ["Link 1", "Link 2", "Link 3"],
        "Link 3 - expandable":
        ["Link 1", "Link 2", "Link 3"]
    },
        ["Link 1 (not expandable)"])
]


@pytest.mark.parametrize("sample", NAVS, ids=lambda sample: sample[0])
def test_navigation(browser, sample):
    locator, tree, currently_selected = sample
    nav = Navigation(browser, locator=locator)
    assert nav.currently_selected == currently_selected
    assert nav.nav_item_tree() == tree


def test_navigation_select(browser):
    loc = ".//h1[normalize-space(.)='Nav Mixed']/following-sibling::section//nav"
    nav = Navigation(browser, locator=loc)
    nav.select("Link 3 - expandable", "Link 2")
    assert nav.currently_selected == ["Link 3 - expandable", "Link 2"]
    nav.select("Link 1 (not expandable)")
    assert nav.currently_selected == ["Link 1 (not expandable)"]
