from widgetastic_patternfly4 import DonutChart


CATEGORY = "charts"


def test_donut(browser):
    donut_chart = DonutChart(browser, locator=".//div[@class='donut-chart-inline']")
    assert donut_chart.donut.labels == ["100", "Pets"]
    assert donut_chart.legend.all_items == [
        {"label": "Cats", "value": None},
        {"label": "Dogs", "value": None},
        {"label": "Birds", "value": None},
    ]
    assert donut_chart.legend.item("Cats").label == "Cats"
