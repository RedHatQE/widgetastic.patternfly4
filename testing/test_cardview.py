import pytest
from wait_for import wait_for
from widgetastic.widget import ParametrizedView
from widgetastic.widget import Text
from widgetastic.widget import View

from widgetastic_patternfly4 import CardCheckBox
from widgetastic_patternfly4 import CardForCardGroup
from widgetastic_patternfly4 import CardGroup
from widgetastic_patternfly4 import Dropdown

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/card/react-demos/card-view"


class PageCard(CardForCardGroup,):
    def __init__(self, parent, locator=None, logger=None, **kwargs):
        super().__init__(parent, locator=locator, logger=logger, **kwargs)
        # workaround for overlapping bottom paginator
        # TODO fix it in widgetastic.core
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", self.__element__()
        )

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


def test_read_and_drop_first_card(cards):

    first = next(iter(cards))

    assert first.header_text.read() == "Patternfly"

    first.delete_action()

    new_first = next(iter(cards))

    assert new_first.header_text.read() != "Patternfly"


def read_cards_2_checkmap(cards):
    data = cards.cards.read()
    return {card["header_text"]: card["checked"] for card in data.values()}


def test_select_all_cards(cards):

    name2checked = read_cards_2_checkmap(cards)
    assert not any(name2checked.values())

    for card in cards:
        card.checked.fill(True)

    name2checked_after = read_cards_2_checkmap(cards)
    assert all(name2checked_after.values())

    assert name2checked.keys() == name2checked_after.keys()
