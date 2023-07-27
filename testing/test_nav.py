import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import Navigation
from widgetastic_patternfly4 import NavSelectionNotFound

TESTING_PAGE_URL = "https://patternfly-react-main.surge.sh/components/navigation"

NAVS = [
    (
        ".//div[@id='ws-react-c-navigation-default']",
        ["Default Link 1", "Default Link 2", "Default Link 3", "Default Link 4"],
        ["Default Link 1"],
        "default",
    ),
    (
        ".//div[@id='ws-react-c-navigation-expandable']",
        {
            "Expandable Group 1": ["Subnav 1 Link 1", "Subnav 1 Link 2", "Subnav 1 Link 3"],
            "Expandable Group 2": [
                "Custom onClick Link",
                "Subnav 2 Link 1",
                "Subnav 2 Link 2",
                "Subnav 2 Link 3",
            ],
        },
        ["Expandable Group 1", "Subnav 1 Link 1"],
        "expandable",
    ),
    (
        ".//div[@id='ws-react-c-navigation-mixed']",
        {
            "Link 1 (not expandable)": None,
            "Expandable section title 1": ["Mixed Link 1", "Mixed Link 2", "Mixed Link 3"],
            "Expandable section title 2": ["Mixed 2 Link 1", "Mixed 2 Link 2", "Mixed 2 Link 3"],
        },
        ["Link 1 (not expandable)"],
        "mixed",
    ),
]


@pytest.fixture(params=NAVS, ids=lambda sample: sample[3])
def data(browser, request):
    locator, tree, currently_selected, _ = request.param

    class TestView(View):
        ROOT = locator

        nav = Navigation(locator="./nav")

    return TestView(browser).nav, tree, currently_selected


def test_navigation(browser, data):
    nav, tree, currently_selected = data
    assert nav.currently_selected == currently_selected
    assert nav.nav_item_tree() == tree


def test_navigation_select(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-navigation-mixed']"
        nav = Navigation(locator="./nav")

    nav = TestView(browser).nav
    nav.select("Expandable section title 2", "Mixed 2 Link 2")
    assert nav.currently_selected == ["Expandable section title 2", "Mixed 2 Link 2"]
    nav.select("Link 1 (not expandable)")
    assert nav.currently_selected == ["Link 1 (not expandable)"]

    # try to select some bogus location and make sure proper exception is raised
    with pytest.raises(NavSelectionNotFound):
        nav.select("This location does not exist")
