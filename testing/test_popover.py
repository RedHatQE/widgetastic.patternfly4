import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import Popover
from widgetastic_patternfly4.button import Button

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/popover"
PF4_EXAMPLE_POPOVER_TEXT_TITLE = "Popover header"
PF4_EXAMPLE_POPOVER_TEXT_BODY = "Popovers are triggered by click rather than hover."
PF4_EXAMPLE_POPOVER_TEXT_FOOTER = "Popover footer"


@pytest.fixture()
def popover(browser):
    class TestView(View):
        ROOT = ".//body"
        popover = Popover()
        open_button = Button("Toggle Popover")

    view = TestView(browser)
    view.open_button.click()
    yield view.popover
    if view.popover.is_displayed:
        view.popover.close()


def test_popover_is_displayed(popover):
    assert popover.is_displayed


def test_popover_title_text_accessible(popover):
    assert popover.title == PF4_EXAMPLE_POPOVER_TEXT_TITLE


def test_popover_body_text_accessible(popover):
    assert popover.body == PF4_EXAMPLE_POPOVER_TEXT_BODY


def test_popover_footer_text_accessible(popover):
    assert popover.footer == PF4_EXAMPLE_POPOVER_TEXT_FOOTER


def test_popover_close(popover):
    popover.close()
    assert not popover.is_displayed
