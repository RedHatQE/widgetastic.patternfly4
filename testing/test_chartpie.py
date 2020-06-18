from time import sleep

import pytest

from widgetastic_patternfly4 import PieChart
from widgetastic_patternfly4.bulletchart import DataPoint
from widgetastic_patternfly4.bulletchart import Legend

CATEGORY = "charts"

DATA = {"Cats": 35, "Dogs": 55, "Birds": 10}
LEGENDS = [Legend(label, value) for label, value in DATA.items()]
DATA_POINTES = [DataPoint(label, value) for label, value in DATA.items()]


@pytest.fixture(
    params=[
        "ws-react-c-chartpie-multi--color-ordered-with-bottom-aligned-legend",
        "ws-react-c-chartpie-basic-with-right-aligned-legend",
    ],
    ids=["bottom-aligned", "right-aligned"],
)
def chart(browser, request):
    sleep(3)  # Stabilized graph data on testing page; specially for firefox.
    return PieChart(browser, id=request.param)


def test_pie_chart(chart):
    """Test PieChart widget."""
    assert chart.is_displayed
    assert chart.legends == LEGENDS
    assert chart.data == DATA_POINTES
    assert "Birds" in chart.legend_names

    # get data point and check values
    birds_legend = chart.get_legend("Birds")
    birds_data = chart.get_data_point("Birds")

    assert birds_data.label == birds_legend.label
    assert birds_data.value == birds_legend.value
    assert birds_data.color == birds_legend.color

    # read graph
    assert chart.read() == DATA
