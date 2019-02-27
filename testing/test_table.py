import pytest
from widgetastic_patternfly4 import PatternflyTable
from widgetastic.widget import Checkbox


SORT = [
    ("Repositories", "ascending", ["a", "one", "p"]),
    ("Repositories", "descending", ["p", "one", "a"]),
    ("Pull requests", "ascending", ["a", "b", "k"]),
    ("Pull requests", "descending", ["k", "b", "a"])
]


@pytest.mark.parametrize("sample", SORT, ids=lambda sample: "{}-{}".format(sample[0], sample[1]))
def test_sortable_table(browser, sample):
    header, order, expected_result = sample
    table = PatternflyTable(browser, ".//table[./caption[normalize-space(.)='Sortable Table']]")
    table.sort_by(header, order)
    column = [row[header] for row in table.read()]
    assert column == expected_result


@pytest.mark.parametrize(
    "sample",
    [("select_all", True), ("deselect_all", False)],
    ids=("select", "deselect")
)
def test_selectable_table(browser, sample):
    method, expected_result = sample
    table = PatternflyTable(
        browser,
        ".//table[./caption[normalize-space(.)='Selectable Table']]",
        column_widgets={0: Checkbox(locator=".//input")}
    )
    getattr(table, method)()
    for row in table:
        assert expected_result == row[0].widget.selected
