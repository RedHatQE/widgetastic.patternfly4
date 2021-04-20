import pytest
from wait_for import wait_for
from widgetastic.widget import ParametrizedView
from widgetastic.widget import Text
from widgetastic.widget import View

from widgetastic_patternfly4 import CardCheckBox
from widgetastic_patternfly4 import CardForCardGroup
from widgetastic_patternfly4 import CardGroup
from widgetastic_patternfly4 import Dropdown

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/demos/card-view/react-demos/card-view/"


class PageCard(CardForCardGroup,):
    dropdown = Dropdown()

    def delete_action(self):
        self.dropdown.item_select("Delete")

    checked = CardCheckBox()

    header_text = Text(locator="./div[@class='pf-c-card__title']")


class Cards(CardGroup):
    def __init__(self, parent, locator=None, logger=None, **kwargs):
        View.__init__(self, parent, logger=logger, **kwargs)
        self.locator = locator or './/div[contains(@class, "pf-l-gallery")]'

    cards = ParametrizedView.nested(PageCard)


@pytest.fixture
def cards(browser):

    cards = Cards(browser)
    wait_for(lambda: cards.is_displayed, timeout="15s")
    return cards


def test_read_and_drop_second_card(cards):
    second = list(cards)[1]

    assert second.header_text.read() == "Patternfly"

    second.delete_action()

    new_second = list(cards)[1]

    assert new_second.header_text.read() != "Patternfly"


def read_cards_2_checkmap(cards):
    data = cards.cards.read()
    return {card["header_text"]: card["checked"] for card in list(data.values())[1:]}


def test_select_all_cards(browser, cards):

    name2checked = read_cards_2_checkmap(cards)
    assert not any(name2checked.values())

    # first card doesn't have header and checkbox
    for card in list(cards)[1:]:
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", card.checked)
        card.checked.fill(True)

    name2checked_after = read_cards_2_checkmap(cards)
    assert all(name2checked_after.values())

    assert name2checked.keys() == name2checked_after.keys()
