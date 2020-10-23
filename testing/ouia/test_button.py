import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import ButtonOUIA

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/button"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-button-ouia']"
        button = ButtonOUIA("Primary")

    return TestView(browser)


def test_button_click(view):
    assert view.button.is_displayed
    view.button.click()
