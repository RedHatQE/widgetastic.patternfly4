import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import Navigation

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/nav"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-nav-ouia']"
        nav = Navigation("Nav Default")

    return TestView(browser)


def test_navigation(browser, view):
    assert view.nav.currently_selected == ["Link 1"]
    assert view.nav.nav_item_tree() == ["Link 1", "Link 2", "Link 3", "Link 4"]
