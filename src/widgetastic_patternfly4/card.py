from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Checkbox
from widgetastic.widget import GenericLocatorWidget
from widgetastic.widget import ParametrizedView
from widgetastic.widget import View


class Card(GenericLocatorWidget):
    def __init__(self, parent, locator=None, logger=None, **kwargs):
        View.__init__(self, parent, logger=logger, **kwargs)
        self.locator = locator or ".//article[contains(@class, 'pf-c-card')]"

    ROOT = ParametrizedLocator("{@locator}")


class CardForCardGroup(ParametrizedView):
    def __init__(self, parent, locator=None, logger=None, **kwargs):
        View.__init__(self, parent, logger=logger, **kwargs)
        self.locator = locator or ".//article[contains(@class, 'pf-c-card')]"

    PARAMETERS = ("position",)

    ROOT = ParametrizedLocator("{@locator}[{position}]")

    def __locator__(self):
        return self.ROOT

    @classmethod
    def all(cls, browser):
        # todo: OUIA versions should return component ids
        elements = browser.elements("./article")
        result = []
        for index, item in enumerate(elements):
            result.append((index + 1,))
        return result


class CardGroup(GenericLocatorWidget, View):
    def __init__(self, parent, locator=None, logger=None, **kwargs):
        View.__init__(self, parent, logger=logger, **kwargs)
        self.locator = locator or './/section[@class="pf-c-page__main-section"]/div'

    cards = ParametrizedView.nested(CardForCardGroup)

    def __iter__(self):
        return iter(self.cards)


class CardCheckBox(Checkbox):
    ROOT = ".//input[@class='pf-c-check__input']"
