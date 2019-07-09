import re

from widgetastic.widget import (
    Widget,
    View,
    ParametrizedLocator,
    ParametrizedView,
    ClickableMixin,
)
from widgetastic.xpath import quote

LEGEND_DETAIL = re.compile(r"(.*?): ([\d]+)")


def _get_legend_item(text):
    match = LEGEND_DETAIL.match(text)
    if match:
        return match.group(1), match.group(2)
    else:
        return text, None


class DonutChart(View):
    """
        Represents the Donut Chart
        from Patternfly 4 (https://www.patternfly.org/v4/documentation/react/charts/chartdonut)
    """

    ROOT = ParametrizedLocator("{@locator}")
    BASE_LOCATOR = ".//div[@id={}]"

    def __init__(self, parent, id=None, locator=None, logger=None):
        """Create the widget"""
        Widget.__init__(self, parent, logger=logger)
        if id:
            self.locator = self.BASE_LOCATOR.format(quote(id))
        elif locator:
            self.locator = locator
        else:
            raise TypeError("You need to specify either id or locator")

    @View.nested
    class donut(View):  # noqa
        ROOT = ".//div[*[name()='svg'][*[name()='text'] and not(*[name()='rect'])]]"
        LABELS_LOCATOR = "./*[name()='svg']/*[name()='text']/*[name()='tspan']"

        @property
        def labels(self):
            return [self.browser.text(elem) for elem in self.browser.elements(self.LABELS_LOCATOR)]

    @View.nested
    class legend(View):  # noqa
        ROOT = "./div[contains(@class, 'VictoryContainer')]"
        ALL_ITEMS = "./*[name()='svg']/*[name()='g']/*[name()='text']/*[name()='tspan']"

        @ParametrizedView.nested
        class item(ParametrizedView, ClickableMixin):  # noqa
            PARAMETERS = ("label_text",)
            ROOT = ParametrizedLocator(
                ".//*[name()='svg']/*[name()='g']/*[name()='text']"
                "/*[name()='tspan' and contains(., '{label_text}')]"
            )

            @property
            def label(self):
                return _get_legend_item(self.browser.text(self))[0]

            @property
            def value(self):
                return _get_legend_item(self.browser.text(self))[1]

        @property
        def all_items(self):
            els = self.browser.elements(self.ALL_ITEMS)
            result = []
            for el in els:
                label, value = _get_legend_item(self.browser.text(el))
                result.append({"label": label, "value": value})
            return result
