from conftest import CustomBrowser

import pytest
from widgetastic.widget import View
from widgetastic_patternfly4 import Button


@pytest.fixture
def browser(selenium):
    selenium.get("http://patternfly-react.netlify.com/components/button")
    return CustomBrowser(selenium)


def test_button_click(browser):
    class TestView(View):
        any_button = Button()
        button1 = Button("Primary")
        button2 = Button("Link to Core Docs")
        button3 = Button(title='noText', classes=[Button.PRIMARY])

    view = TestView(browser)
    assert view.any_button.is_displayed
    assert view.button1.is_displayed
    assert view.button2.is_displayed
    # assert view.button3.is_displayed