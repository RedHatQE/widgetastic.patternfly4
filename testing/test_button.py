import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import Button

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/button"


@pytest.fixture
def variations_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-button-variations']"
        any_button = Button()
        button1 = Button("Primary")

    return TestView(browser)


@pytest.fixture
def disabled_view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-button-disabled']"
        button = Button("Primary disabled")

    return TestView(browser)


def test_button_click(variations_view):
    assert variations_view.any_button.is_displayed
    assert variations_view.button1.is_displayed


def test_disabled_button(disabled_view):
    assert disabled_view.button.is_displayed
    assert disabled_view.button.disabled
