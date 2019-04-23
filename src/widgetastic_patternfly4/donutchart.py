import re

from widgetastic.widget import (
    Widget,
    View,
    ParametrizedLocator,
    ParametrizedView,
    ClickableMixin,
    Text,
)
from widgetastic.xpath import quote

LEGEND_DETAIL = re.compile(r"(.*?) \(([\d]+)\)")


def _get_legend_item(text):
    match = LEGEND_DETAIL.match(text)
    if match:
        return match.group(1), match.group(2)
    else:
        return text, None


class DonutChart(View):
    """
        Represents the Donut Chart
        from Patternfly 4 (https://patternfly-react.surge.sh/patternfly-4/components/donutchart)
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
        ROOT = ".//div[contains(@class, 'chart-container')]"
        label = Text(
            locator="(.//*[name()='svg' and contains(@class, 'chart-label')]"
            "/*[name()='text']/*[name()='tspan'])[1]"
        )

        @property
        def total(self):
            try:
                return int(self.label.text)
            except ValueError:
                return None

    @View.nested
    class legend(View):  # noqa
        ROOT = (
            ".//div[contains(@class, 'VictoryContainer') "
            "and not(ancestor::div[contains(@class, 'chart-container')])]"
        )
        ALL_ITEMS = "./*[name()='svg']/*[name()='text']/*[name()='tspan']"

        @ParametrizedView.nested
        class item(ParametrizedView, ClickableMixin):  # noqa
            PARAMETERS = ("label_text",)
            ROOT = ParametrizedLocator(
                ".//*[name()='svg']/*[name()='text']"
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
