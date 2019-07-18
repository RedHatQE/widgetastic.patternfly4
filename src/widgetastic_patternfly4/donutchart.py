import re

from widgetastic.widget import (
    Widget,
    View,
    ParametrizedLocator,
    ParametrizedView,
    ClickableMixin,
)
from widgetastic.xpath import quote


class DonutLegendItem(ParametrizedView, ClickableMixin):
    PARAMETERS = ("label_text",)
    ROOT = ParametrizedLocator(
        ".//*[name()='svg']/*[name()='g']/*[name()='text']"
        "/*[name()='tspan' and contains(., '{label_text}')]"
    )
    ALL_ITEMS = "./*[name()='svg']/*[name()='g']/*[name()='text']/*[name()='tspan']"
    LEGEND_ITEM_REGEX = re.compile(r"(.*?): ([\d]+)")

    @classmethod
    def _get_legend_item(cls, text):
        match = cls.LEGEND_ITEM_REGEX.match(text)
        if match:
            return match.group(1), match.group(2)
        else:
            return text, None

    @property
    def label(self):
        return self._get_legend_item(self.browser.text(self))[0]

    @property
    def value(self):
        return self._get_legend_item(self.browser.text(self))[1]

    @classmethod
    def all(cls, browser):
        return [(browser.text(el),) for el in browser.elements(cls.ALL_ITEMS)]


class DonutLegend(View):
    ROOT = "./div[contains(@class, 'VictoryContainer')]"

    item = ParametrizedView.nested(DonutLegendItem)

    @property
    def all_items(self):
        result = []
        for i in self.item:
            result.append({"label": i.label, "value": i.value})
        return result


class DonutCircle(View):
    ROOT = ".//div[*[name()='svg'][*[name()='text'] and not(*[name()='rect'])]]"
    LABELS_LOCATOR = "./*[name()='svg']/*[name()='text']/*[name()='tspan']"

    @property
    def labels(self):
        return [self.browser.text(elem) for elem in self.browser.elements(self.LABELS_LOCATOR)]


class DonutChart(View):
    """
    Represents the Donut Chart
    from Patternfly 4 (https://www.patternfly.org/v4/documentation/react/charts/chartdonut)
    """

    ROOT = ParametrizedLocator("{@locator}")
    BASE_LOCATOR = ".//div[@id={}]"

    donut = View.nested(DonutCircle)
    legend = View.nested(DonutLegend)

    def __init__(self, parent, id=None, locator=None, logger=None):
        """Create the widget"""
        Widget.__init__(self, parent, logger=logger)
        if id:
            self.locator = self.BASE_LOCATOR.format(quote(id))
        elif locator:
            self.locator = locator
        else:
            raise TypeError("You need to specify either id or locator")
