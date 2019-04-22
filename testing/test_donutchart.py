import pytest

from widgetastic_patternfly4 import DonutChart


@pytest.mark.skip("Donut widget is currently broken")
def test_donut(browser):
    donut_chart = DonutChart(browser, locator=".//div[contains(@class, 'chart-inline')]")
    assert donut_chart.donut.total == 100
    assert donut_chart.legend.all_items == [
        {"label": "Cats", "value": None},
        {"label": "Dogs", "value": None},
        {"label": "Birds", "value": None}
    ]
    assert donut_chart.legend.item("Cats").label == "Cats"
