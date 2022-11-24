from time import sleep

import pytest

from widgetastic_patternfly4 import LineChart

TESTING_PAGE_URL = (
    "https://www.patternfly.org/v4/charts/line-chart/react/green-with-bottom-aligned-legend/"
)

TEST_DATA = {
    "2015": {"Cats": "1", "Dogs": "2", "Birds": "3", "Mice": "3"},
    "2016": {"Cats": "2", "Dogs": "1", "Birds": "4", "Mice": "3"},
    "2017": {"Cats": "5", "Dogs": "7", "Birds": "9", "Mice": "8"},
    "2018": {"Cats": "3", "Dogs": "4", "Birds": "5", "Mice": "7"},
}


@pytest.fixture()
def chart(browser):
    sleep(3)  # Stabilized graph data on testing page; specially for firefox.
    return LineChart(browser, id="ws-react-c-line-chart-green-with-bottom-aligned-legend")


def test_line_chart(chart):
    """Test LineChart widget."""

    assert chart.is_displayed
    expected_legends = list(TEST_DATA.values())[0].keys()

    for leg, expected_leg in zip(chart.legends, expected_legends):
        assert leg.label == expected_leg

    assert set(chart.legend_names) == set(expected_legends)

    # get data point and check values
    birds_legend = chart.get_legend("Birds")
    assert birds_legend.label == "Birds"
    assert birds_legend.color == "rgb(35, 81, 30)"

    # read graph
    assert chart.read() == TEST_DATA
