import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import Button

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/button"

pytestmark = pytest.mark.skip("No OUIA IDs provided on Patternfly testing page")


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-button-ouia']"
        button = Button("Primary")

    return TestView(browser)


def test_button_click(view):
    view.button.__repr__()
    assert view.button.is_displayed
    view.button.click()
