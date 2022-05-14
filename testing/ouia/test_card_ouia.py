import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import Card

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/card"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-card-basic']"
        card = Card("352")

    return TestView(browser)


def test_card_displayed(view):
    assert view.card.is_displayed
