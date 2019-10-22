import re

from widgetastic.widget import ClickableMixin
from widgetastic.widget import ParametrizedLocator
from widgetastic.widget import ParametrizedView
from widgetastic.widget import View
from widgetastic.widget import Widget
from widgetastic.xpath import quote


class DonutLegendItem(ParametrizedView, ClickableMixin):
    PARAMETERS = ("label_text",)
    ROOT = ParametrizedLocator(
        ".//*[name()='text']" "/*[name()='tspan' and contains(., '{label_text}')]"
    )
    ALL_ITEMS = ".//*[name()='text']/*[name()='tspan']"
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
        """Returns the label of a DonutLegendItem as a string"""
        return self._get_legend_item(self.browser.text(self))[0]

    @property
    def value(self):
        """Returns the value of a DonutLegendItem as a string"""
        return self._get_legend_item(self.browser.text(self))[1]

    @classmethod
    def all(cls, browser):
        """Returns a list of all items"""
        return [(browser.text(el),) for el in browser.elements(cls.ALL_ITEMS)]


class DonutLegend(View):
    ROOT = ".//*[name()='g'][2]"

    item = ParametrizedView.nested(DonutLegendItem)

    @property
    def all_items(self):
        """Returns a list of all items, arranged as {label: value}"""
        result = []
        for i in self.item:
            result.append({"label": i.label, "value": i.value})
        return result


class DonutCircle(View):
    ROOT = ".//div[*[name()='svg'][*[name()='text'] and not(*[name()='rect'])]]"
    LABELS_LOCATOR = "./*[name()='svg']/*[name()='text']/*[name()='tspan']"

    @property
    def labels(self):
        """Returns a list of labels"""
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
