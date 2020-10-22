import re

from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Text
from widgetastic.widget import View
from widgetastic.xpath import quote


class Legend:
    """Represents Legend of chart."""

    def __init__(self, label, value=None, color=None, element=None):
        self.label = label
        self.value = value
        self.color = color
        self.element = element

    def click(self):
        self.element.click()

    def __repr__(self):
        return f"Legend({self.label}: {self.value})"

    def __gt__(self, leg):
        return self.__class__ == leg.__class__ and self.value > leg.value

    def __eq__(self, leg):
        return (
            self.__class__ == self.__class__ and self.label == leg.label and self.value == leg.value
        )


class DataPoint(Legend):
    """Represents DataPoint on chart."""

    def __repr__(self):
        return f"DataPoint({self.label}: {self.value})"


class BulletChart(View):
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
    LEGEND_ITEM_REGEX = re.compile(r"(\d+)\s(\w.*)|(\w.*)\s(\d+)")

    ITEMS = ".//*[name()='g']/*[name()='path' and not(contains(@style, 'type:square'))]"
    TOOLTIP_REGEX = re.compile(r"(.*?): ([\d]+)")
    APPLY_OFFSET = True

    tooltip = Text(
        ".//*[name()='svg' and contains(@aria-labelledby, 'victory-container')]/"
        "following-sibling::div[contains(@style, 'z-index')]/*[name()='svg']"
    )

    def __init__(self, parent=None, id=None, locator=None, logger=None, *args, **kwargs):
        View.__init__(self, parent=parent, logger=logger)
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
        size = self.browser.size_of(el)
        width = size.width
        height = size.height
        dx = int(width / offset_denominator) if (width > 10 and height > 10) else 0
        dy = int(height / offset_denominator) if (width > 10 and height > 10) else 0
        return dx, dy

    @property
    def legends(self):
        """Return all Legend objects."""

        br = self.browser
        _data = []
        for (icon, label_el) in zip(br.elements(self.LEGEND_ICON), br.elements(self.LEGEND_TEXT)):
            label_text = br.text(label_el)
            match = self.LEGEND_ITEM_REGEX.match(label_text)
            if match:
                left_value, left_label, right_label, right_value = match.groups()
            label = right_label or left_label if match else label_text
            value = int(right_value or left_value) if match else None
            _data.append(
                Legend(
                    label=label,
                    value=value,
                    color=icon.value_of_css_property("fill"),
                    element=label_el,
                )
            )
        return _data

    @property
    def legend_names(self):
        """Return all legend names."""
        return [leg.label for leg in self.legends]

    def get_legend(self, label):
        """Get specific Legend object.

        Args:
            label: Name of legend label.
        """
        try:
            return next(leg for leg in self.legends if leg.label == label)
        except StopIteration:
            return None

    @property
    def data(self):
        """Read graph and returns all Data Point objects."""
        _data = []
        # focus away from graph
        self.parent_browser.move_to_element("//body")

        for el in self.browser.elements(self.ITEMS):
            self.browser.move_to_element(el)

            if self.APPLY_OFFSET:
                dx, dy = self._offsets(el)
                self.browser.move_by_offset(dx, dy)

            match = self.TOOLTIP_REGEX.match(self.tooltip.text)
            if match:
                _data.append(
                    DataPoint(
                        label=match.groups()[0],
                        value=int(match.groups()[1]),
                        color=el.value_of_css_property("fill"),
                        element=el,
                    )
                )
        return _data

    def get_data_point(self, label):
        """Get specific data point object.

        Args:
            label: Name of respective data point label.
        """
        try:
            return next(dp for dp in self.data if dp.label == label)
        except StopIteration:
            return None

    def read(self):
        """Read graph and returns label, value dict."""
        return {dp.label: dp.value for dp in self.data}
