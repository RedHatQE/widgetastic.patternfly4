from widgetastic.widget import ParametrizedLocator
from widgetastic.widget import View
from widgetastic.xpath import quote

from widgetastic_patternfly4.bulletchart import Legend


class LineChart(View):
    """Represents the Patternfly Line Chart.

    https://www.patternfly.org/v4/charts/line-chart/react/green-with-bottom-aligned-legend/

    Args:
        id: If you want to look the input up by id, use this parameter, pass the id.
        locator: If you have specific locator else it will take pf-chart.
    """

    ROOT = ParametrizedLocator("{@locator}")

    X_AXIS_LABELS = "(.//*[name()='g' and *[name()='line'] and *[name()='g']])[1]//*[name()='text']"
    Y_AXIS_LABELS = "(.//*[name()='g' and *[name()='line'] and *[name()='g']])[2]//*[name()='text']"

    TOOLTIP = (
        ".//*[name()='g' and .//*[name()='g' and "
        ".//*[name()='text' and contains(@id, 'legend-labels')]]]"
    )

    TOOLTIP_X_AXIS_LABLE = ".//*[name()='text']"
    TOOLTIP_LABLES = ".//*[name()='g']/*[name()='text' and not(contains(@id, 'legend-label'))]"
    TOOLTIP_VALUES = ".//*[name()='g']/*[name()='text' and contains(@id, 'legend-label')]"

    _legends = View.nested(Legend)

    def __init__(self, parent=None, id=None, locator=None, logger=None):
        View.__init__(self, parent=parent, logger=logger)

        assert id or locator, "Provide id or locator."

        if id:
            self.locator = ".//div[@id={}]".format(quote(id))
        else:
            self.locator = locator

    @property
    def legends(self):
        """Return object of Legends"""
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
    def _x_axis_labels_map(self):
        return {self.browser.text(el): el for el in self.browser.elements(self.X_AXIS_LABELS)}

    @property
    def labels_x_axis(self):
        """Return X-Axis labels."""
        return list(self._x_axis_labels_map.keys())

    def read(self, offset=(0, -100)):
        """Read chart data.

        Note: This method has some limitations as we are reading the tooltip for x-axis labels
        with some offset. So only applicable for the chart which shows all Legend data in a single
        tooltip for the respective x-axis label.

        Args:
            offset: offset to move the cursor from the x-axis label so that the tooltip can appear.
        """
        _data = {}

        for lab_el in self._x_axis_labels_map.values():
            self.browser.move_to_element(lab_el)
            self.browser.click(lab_el)
            self.browser.move_by_offset(*offset)
            tooltip_el = self.browser.wait_for_element(self.TOOLTIP)

            x_axis_label = self.browser.text(self.TOOLTIP_X_AXIS_LABLE, parent=tooltip_el)
            label_data = {}

            for label_el, value_el in zip(
                self.browser.elements(self.TOOLTIP_LABLES, parent=tooltip_el),
                self.browser.elements(self.TOOLTIP_VALUES, parent=tooltip_el),
            ):
                label_data[self.browser.text(label_el)] = self.browser.text(value_el)

            _data[x_axis_label] = label_data

        # Just move cursor to avoid mismatch of legend and tooltip text.
        self.root_browser.move_to_element(".//body")
        return _data
