import pytest

from widgetastic.browser import Browser

from widgetastic_patternfly4 import DonutChart


@pytest.fixture(scope="module")
def browser(selenium):
    selenium.maximize_window()
    selenium.get("http://patternfly-react.surge.sh/patternfly-4/charts/chartdonut")
    return Browser(selenium)


def test_donut(browser):
    donut_chart = DonutChart(browser, locator=".//div[@class='donut-chart-inline']")
    assert donut_chart.donut.labels == ["100", "Pets"]
    assert donut_chart.legend.all_items == [
        {"label": "Cats", "value": None},
        {"label": "Dogs", "value": None},
        {"label": "Birds", "value": None},
    ]
    assert donut_chart.legend.item("Cats").label == "Cats"
