import re

from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import ParametrizedView
from widgetastic.widget import Text
from widgetastic.widget import View
from widgetastic.xpath import quote


class Legend(ParametrizedView):
    """Represents Legend of chart."""

    PARAMETERS = ("label_text",)

    LEGEND_LABEL = ParametrizedLocator(
        ".//*[name()='text' and (contains(@id, 'legend') or contains(@id, 'Legend'))]"
        "/*[name()='tspan' and contains(., {label_text|quote})]"
    )
    ROOT = ParametrizedLocator(".//*[name()='g' and {@LEGEND_LABEL}]")
    LEGEND_LABEL_ITEMS = (
        ".//*[name()='text' and (contains(@id, 'legend') or "
        "contains(@id, 'Legend'))]/*[name()='tspan']"
    )
    LEGEND_ICON_ITEMS = ".//*[name()='rect']/following-sibling::*[name()='path']"

    # Need to overwrite as per need.
    LEGEND_ITEM_REGEX = re.compile(r"(\d+)\s(\w.*)|(\w.*)\s(\d+)")

    @property
    def _legend_color_map(self):
        _data = {}

        for icon, label_el in zip(
            self.browser.elements(self.LEGEND_ICON_ITEMS),
            self.browser.elements(self.LEGEND_LABEL_ITEMS),
        ):
            color = icon.value_of_css_property("fill")
            if not color:
                color = icon.value_of_css_property("color")
            _data[self.browser.text(label_el)] = color
        return _data

    @classmethod
    def _get_legend_item(cls, text):
        text = text.replace(":", "")
        match = cls.LEGEND_ITEM_REGEX.match(text)

        if match:
            left_value, left_label, right_label, right_value = match.groups()
            label = right_label or left_label if match else text
            value = int(right_value or left_value) if match else None
            return label, value
        else:
            return text, None

    @property
    def label(self):
        """Returns the label of a Legend"""
        return self._get_legend_item(self.browser.text(self.LEGEND_LABEL))[0]

    @property
    def value(self):
        """Returns the value of a Legend"""
        return self._get_legend_item(self.browser.text(self.LEGEND_LABEL))[1]

    @property
    def color(self):
        """Returns the color of a Legend"""
        return self._legend_color_map.get(self.browser.text(self.LEGEND_LABEL))

    def click(self):
        """Click on a Legend"""
        self.browser.click(self.LEGEND_LABEL)

    @classmethod
    def all(cls, browser):
        """Returns a list of all items"""
        return [(browser.text(el),) for el in browser.elements(cls.LEGEND_LABEL_ITEMS)]

    def __repr__(self):
        return f"Legend({self.browser.text(self.LEGEND_LABEL)})"


class DataPoint:
    """Represents DataPoint on chart."""

    def __init__(self, label, value=None, color=None):
        self.label = label
        self.value = value
        self.color = color

    def __gt__(self, leg):
        return self.__class__ == leg.__class__ and self.value > leg.value

    def __eq__(self, leg):
        return (
            self.__class__ == self.__class__ and self.label == leg.label and self.value == leg.value
        )

    def __repr__(self):
        return f"DataPoint({self.label}: {self.value})"


class BulletChart(View):
    """Represents the Patternfly Bullet Chart.

    https://www.patternfly.org/v4/charts/bullet-chart

    Args:
        id: If you want to look the input up by id, use this parameter, pass the id.
        locator: If you have specific locator else it will take pf-chart.
        offset_denominator: Denominator for offset value calculation.
    """

    ROOT = ParametrizedLocator("{@locator}")

    DEFAULT_LOCATOR = ".//div[contains(@class, 'chartbullet')]"
    ITEMS = ".//*[name()='g']/*[name()='path' and not(contains(@style, 'type:square'))]"
    TOOLTIP_REGEX = re.compile(r"(.*?): ([\d]+)")
    APPLY_OFFSET = True

    tooltip = Text(
        ".//*[name()='svg' and contains(@aria-labelledby, 'victory-container')]/"
        "following-sibling::div[contains(@style, 'z-index')]/*[name()='svg']"
    )
    _legends = View.nested(Legend)

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
        return [leg for leg in self._legends]

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
            self.browser.click(el)

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
