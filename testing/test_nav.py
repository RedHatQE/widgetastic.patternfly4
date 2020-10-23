import os

import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import Navigation

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/navigation"

NAVS = [
    (
        ".//div[@id='ws-react-c-navigation-default']",
        ["Link 1", "Link 2", "Link 3", "Link 4"],
        ["Link 1"],
        "default",
    ),
    (
        ".//div[@id='ws-react-c-navigation-expandable']",
        {
            "Link 1": ["Subnav Link 1", "Subnav Link 2", "Subnav Link 3"],
            "Link 2": ["Custom onClick", "Subnav Link 1", "Subnav Link 2", "Subnav Link 3"],
        },
        ["Link 1", "Subnav Link 1"],
        "expandable",
    ),
    (
        ".//div[@id='ws-react-c-navigation-mixed']",
        {
            "Link 1 (not expandable)": None,
            "Link 2 - expandable": ["Link 1", "Link 2", "Link 3"],
            "Link 3 - expandable": ["Link 1", "Link 2", "Link 3"],
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


@pytest.mark.xfail(
    os.environ.get("BROWSER") == "firefox",
    reason="Requires https://github.com/RedHatQE/widgetastic.core/pull/182",
)
def test_navigation_select(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-navigation-mixed']"
        nav = Navigation(locator="./nav")

    nav = TestView(browser).nav
    nav.select("Link 3 - expandable", "Link 2")
    assert nav.currently_selected == ["Link 3 - expandable", "Link 2"]
    nav.select("Link 1 (not expandable)")
    assert nav.currently_selected == ["Link 1 (not expandable)"]
