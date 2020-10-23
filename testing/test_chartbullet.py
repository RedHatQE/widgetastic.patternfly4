from time import sleep

import pytest

from widgetastic_patternfly4 import BulletChart
from widgetastic_patternfly4.bulletchart import DataPoint
from widgetastic_patternfly4.bulletchart import Legend

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/charts/bullet-chart"

TEST_DATA = {
    "dot": {
        "id": "ws-react-c-chartbullet-bullet-chart-with-primary-measure-dot",
        "anchor": "#bullet-chart-with-primary-measure-dot",
        "bar_data": [
            DataPoint("Range", 75),
            DataPoint("Range", 50),
            DataPoint("Measure", 25),
            DataPoint("Measure", 60),
            DataPoint("Warning", 88),
        ],
        "legend_data": [
            Legend("Measure", 1),
            Legend("Measure", 2),
            Legend("Warning", None),
            Legend("Range", 1),
            Legend("Range", 2),
        ],
    },
    "tick": {
        "id": "ws-react-c-chartbullet-error-measure-and-custom-axis-ticks",
        "anchor": "#error-measure-and-custom-axis-ticks",
        "bar_data": [
            DataPoint("Range", 150),
            DataPoint("Range", 100),
            DataPoint("Range", 65),
            DataPoint("Measure", 75),
            DataPoint("Measure", 25),
            DataPoint("Error", 120),
            DataPoint("Warning", 80),
        ],
        "legend_data": [
            Legend("Measure", 1),
            Legend("Measure", 2),
            Legend("Warning", None),
            Legend("Error", None),
            Legend("Range", 1),
            Legend("Range", 2),
        ],
    },
}


@pytest.fixture(params=TEST_DATA.keys())
def chart_data(browser, request):
    sleep(3)  # Stabilized graph data on testing page; specially for firefox.
    # Firefox fails the test if the chart is not fully visible therefore we click here on anchor
    # in order to properly scroll down
    anchor = browser.element(f".//a[@href='{request.param['anchor']}']")
    browser.click(anchor)
    return (
        BulletChart(browser, id=TEST_DATA[request.param]["id"]),
        TEST_DATA[request.param]["bar_data"],
        TEST_DATA[request.param]["legend_data"],
        request.param,
    )


@pytest.mark.skip(reason="test is flaky")
def test_bullet_chart(chart_data):
    """Test BulletChart widget."""
    chart, bar_data, legend_data, chart_type = chart_data
    assert chart.is_displayed
    assert chart.legends == legend_data
    assert chart.data == bar_data
    assert "Warning" in chart.legend_names
    # get bar and check values
    warning_data = chart.get_data_point("Warning")
    expected_value = 88 if chart_type == "dot" else 80
    assert warning_data.value == expected_value
    assert warning_data.color == "rgb(236, 122, 8)"
    # get bar with wrong label
    assert not chart.get_data_point("foo")
    # get legend for check values
    warning_legend = chart.get_legend("Warning")
    assert warning_legend.value is None
    assert warning_legend.color == "rgb(236, 122, 8)"
    # get legend with wrong label
    assert not chart.get_legend("foo")
