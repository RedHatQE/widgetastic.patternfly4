from widgetastic_patternfly4 import DonutChart


CATEGORY = "charts"


def test_donut(browser):
    donut_chart = DonutChart(
        browser, locator=".//div[@id='ws-react-c-chartdonut-right-aligned-legend']/div"
    )
    assert donut_chart.donut.labels == ["100", "Pets"]
    assert donut_chart.legend.all_items == [
        {"label": "Cats", "value": "35"},
        {"label": "Dogs", "value": "55"},
        {"label": "Birds", "value": "10"},
    ]
    assert donut_chart.legend.item("Cats").label == "Cats"
