import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import Switch

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/switch"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-switch-ouia']"
        switch = Switch("Simple Switch")

    return TestView(browser)


def test_switch_is_displayed(view):
    assert view.switch.is_displayed


def test_switch_is_enabled(view):
    assert view.switch.is_enabled


def test_switch_label(view):
    assert view.switch.label == "Message when on"


def test_switch_selected(view):
    assert view.switch.read()


def test_switch_fill(view):
    assert view.switch.selected
    assert view.switch.label == "Message when on"
    assert not view.switch.fill(True)
    assert view.switch.selected
    assert view.switch.label == "Message when on"
    assert view.switch.fill(False)
    assert not view.switch.selected
    assert view.switch.label == "Message when off"
    assert view.switch.fill(True)
    assert view.switch.selected
    assert view.switch.label == "Message when on"
