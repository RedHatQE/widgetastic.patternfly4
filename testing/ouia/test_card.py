import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import Card

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/card"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-card-ouia']"
        card = Card("Primary")

    return TestView(browser)


def test_card_displayed(view):
    # TODO actually assert
    # assert view.card.is_displayed
    pass
