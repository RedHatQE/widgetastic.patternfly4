import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import DonutChart

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/charts/donut-chart"


@pytest.fixture
def donut_chart(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-donut-chart-right-aligned-legend']"
        donut_chart = DonutChart(locator="./div")

    return TestView(browser).donut_chart


def test_donut(donut_chart):
    assert donut_chart.donut.labels == ["100", "Pets"]
    assert donut_chart.legend.all_items == [
        {"label": "Cats", "value": "35"},
        {"label": "Dogs", "value": "55"},
        {"label": "Birds", "value": "10"},
    ]
    assert donut_chart.legend.item("Cats").label == "Cats"
