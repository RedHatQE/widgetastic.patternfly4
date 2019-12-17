import pytest

from widgetastic_patternfly4 import Navigation


NAVS = [
    (
        ".//div[@id='ws-react-c-nav-default']/nav",
        ["Link 1", "Link 2", "Link 3", "Link 4"],
        ["Link 1"],
    ),
    (
        ".//div[@id='ws-react-c-nav-expandable']/nav",
        {
            "Link 1": ["Subnav Link 1", "Subnav Link 2", "Subnav Link 3"],
            "Link 2": ["Custom onClick", "Subnav Link 1", "Subnav Link 2", "Subnav Link 3"],
        },
        ["Link 1", "Subnav Link 1"],
    ),
    (
        ".//div[@id='ws-react-c-nav-mixed']/nav",
        {
            "Link 1 (not expandable)": None,
            "Link 2 - expandable": ["Link 1", "Link 2", "Link 3"],
            "Link 3 - expandable": ["Link 1", "Link 2", "Link 3"],
        },
        ["Link 1 (not expandable)"],
    ),
]


@pytest.mark.parametrize("sample", NAVS, ids=lambda sample: sample[0])
def test_navigation(browser, sample):
    locator, tree, currently_selected = sample
    nav = Navigation(browser, locator=locator)
    assert nav.currently_selected == currently_selected
    assert nav.nav_item_tree() == tree


@pytest.mark.skip
def test_navigation_select(browser):
    loc = ".//h2[normalize-space(.)='Navigation mixed']/following-sibling::div[1]//nav"
    nav = Navigation(browser, locator=loc)
    nav.select("Link 3 - expandable", "Link 2")
    assert nav.currently_selected == ["Link 3 - expandable", "Link 2"]
    nav.select("Link 1 (not expandable)")
    assert nav.currently_selected == ["Link 1 (not expandable)"]
