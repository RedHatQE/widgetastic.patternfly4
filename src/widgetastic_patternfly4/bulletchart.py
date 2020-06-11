import re

from cached_property import cached_property
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Text
from widgetastic.widget import Widget
from widgetastic.xpath import quote


class Legend:
    """Represents Legend of chart."""

    def __init__(self, label, value=None, color=None, element=None):
        self.label = label
        self.value = value
        self.color = color
        self.element = element

    def __repr__(self):
        return f"Legend({self.label}: {self.value})"

    def __gt__(self, leg):
        return self.__class__ == leg.__class__ and self.value > leg.value

    def __eq__(self, leg):
        return (
            self.__class__ == self.__class__ and self.label == leg.label and self.value == leg.value
        )


class Bar(Legend):
    """Represents Bar of chart."""

    def __repr__(self):
        return f"Bar({self.label}: {self.value})"


class BulletChart(Widget):
    """Represents the Patternfly Bullet Chart.

    https://www.patternfly.org/v4/documentation/react/charts/chartbullet

    Args:
        id: If you want to look the input up by id, use this parameter, pass the id.
        locator: If you have specific locator else it will take pf-chart.
        offset_denominator: Denominator for offset value calculation.
    """

    ROOT = ParametrizedLocator("{@locator}")
    DEFAULT_LOCATOR = ".//div[contains(@class, 'chartbullet')]"
    LEGEND_ICON = (
        ".//*[name()='g' or name()='svg']/*[name()='rect']/following-sibling::*[name()='path']"
    )
    LEGEND_TEXT = ".//*[name()='text' and contains(@id, 'legend-labels')]"
    LEGEND_ITEM_REGEX = re.compile(r"(\w.*)\s(\d+)|(\d+)\s(\w.*)")

    ITEMS = ".//*[name()='g']/*[name()='path' and not(contains(@style, 'type:square'))]"
    TOOLTIP_REGEX = re.compile(r"(.*?): ([\d]+)")

    tooltip = Text(
        ".//*[name()='svg' and contains(@aria-labelledby, 'victory-container')]/"
        "following-sibling::div[contains(@style, 'z-index')]/*[name()='svg']"
    )

    def __init__(self, parent=None, id=None, locator=None, logger=None, *args, **kwargs):
        Widget.__init__(self, parent=parent, logger=logger)
        if id:
            self.locator = ".//div[@id={}]".format(quote(id))
        elif locator:
            self.locator = locator
        else:
            self.locator = self.DEFAULT_LOCATOR

        self.args = args
        self.kwargs = kwargs

    def _offsets(self, el):
        """Calculate offset. Need to set offset with try and error method."""
        offset_denominator = self.kwargs.pop("offset_denominator", 2.5)
        width = el.size["width"]
        height = el.size["height"]
        x = int(width / offset_denominator) if (width > 10 and height > 10) else 0
        y = int(height / offset_denominator) if (width > 10 and height > 10) else 0
        return x, y

    @cached_property
    def _legends_data(self):
        br = self.browser
        _data = []
        for (icon, label_el) in zip(br.elements(self.LEGEND_ICON), br.elements(self.LEGEND_TEXT)):
            label_text = br.text(label_el)
            match = self.LEGEND_ITEM_REGEX.match(label_text)
            if match:
                right_label, right_value, left_value, left_label = match.groups()
            label = right_label or left_label if match else label_text
            value = int(right_value or left_value) if match else None
            _data.append(
                Legend(
                    label=label, value=value, color=icon.value_of_css_property("fill"), element=icon
                )
            )
        return _data

    @property
    def legends(self):
        """Return all Legend objects."""
        return self._legends_data

    @property
    def legend_names(self):
        """Return all legend names."""
        return [leg.label for leg in self._legends_data]

    def get_legend(self, label):
        """Get specific Legend object.
        Arg:
            label: Name of legend label.
        """
        try:
            return next(leg for leg in self.legends if leg.label == label)
        except StopAsyncIteration:
            return None

    @cached_property
    def data(self):
        """Read graph and returns all Bar objects."""
        _data = []
        # point cursor outside graph
        self.browser.raw_click(self)
        # self.parent_browser.raw_click(".//body")

        for el in self.browser.elements(self.ITEMS):
            x_diff, y_diff = self._offsets(el)
            self.browser.move_to_element(el, force_scroll=True)
            self.browser.move_by_offset(x_diff, y_diff)

            match = self.TOOLTIP_REGEX.match(self.tooltip.text)
            if match:
                _data.append(
                    Bar(
                        label=match.groups()[0],
                        value=int(match.groups()[1]),
                        color=el.value_of_css_property("fill"),
                        element=el,
                    )
                )
        return _data

    def get_bar(self, label):
        """Get specific Bar object.
        Arg:
            label: Name of Bar label.
        """
        try:
            return next(bar for bar in self.data if bar.label == label)
        except StopAsyncIteration:
            return None

    def read(self):
        """Read graph and returns label, value dict."""
        return {b.label: b.value for b in self.data}
