import pytest
from widgetastic_patternfly4 import ExpandableTable, PatternflyTable, RowNotExpandable
from widgetastic.widget import Checkbox


SORT = [
    ("Repositories", "ascending", ["a", "one", "p"]),
    ("Repositories", "descending", ["p", "one", "a"]),
    ("Pull requests", "ascending", ["a", "b", "k"]),
    ("Pull requests", "descending", ["k", "b", "a"]),
]


@pytest.mark.parametrize("sample", SORT, ids=lambda sample: "{}-{}".format(sample[0], sample[1]))
def test_sortable_table(browser, sample):
    header, order, expected_result = sample
    table = PatternflyTable(browser, ".//table[./caption[normalize-space(.)='Sortable Table']]")
    table.sort_by(header, order)
    column = [row[header] for row in table.read()]
    assert column == expected_result


@pytest.mark.parametrize(
    "sample", [("select_all", True), ("deselect_all", False)], ids=("select", "deselect")
)
def test_selectable_table(browser, sample):
    method, expected_result = sample
    table = PatternflyTable(
        browser,
        ".//table[./caption[normalize-space(.)='Selectable Table']]",
        column_widgets={0: Checkbox(locator=".//input")},
    )
    getattr(table, method)()
    for row in table:
        assert expected_result == row[0].widget.selected


def test_expandable_table(browser):
    expected_read = [
        {
            "Header cell": "one",
            "Branches": "two",
            "Pull requests": "three",
            "Workspaces": "four",
            "Last Commit": "five",
        },
        {
            "Header cell": "parent - 1",
            "Branches": "two",
            "Pull requests": "three",
            "Workspaces": "four",
            "Last Commit": "five",
        },
        {
            "Header cell": "parent - 2",
            "Branches": "two",
            "Pull requests": "three",
            "Workspaces": "four",
            "Last Commit": "five",
        },
        {
            "Header cell": "parent - 3",
            "Branches": "two",
            "Pull requests": "three",
            "Workspaces": "four",
            "Last Commit": "five",
        },
    ]

    row1_expected_content = "child - 1"
    row2_expected_content = "child - 2"
    row3_expected_content = "child - 3"

    table = ExpandableTable(browser, ".//table[./caption[normalize-space(.)='Collapsible table']]")

    assert table.read() == expected_read

    # First row is not an expandable row
    assert not table[0].is_expandable
    with pytest.raises(RowNotExpandable):
        table[0].expand()

    parent1_row = table[1]
    parent2_row = table[2]
    parent3_row = table[3]

    parent1_row.collapse()  # The row starts out expanded on the demo page
    assert not parent1_row.is_expanded
    assert not parent1_row.content.is_displayed

    parent1_row.expand()
    assert parent1_row.is_expanded
    assert parent1_row.content.is_displayed
    assert parent1_row.content.read() == row1_expected_content

    parent2_row.expand()
    assert parent2_row.is_expanded
    assert parent2_row.content.is_displayed
    assert parent2_row.content.read() == row2_expected_content

    parent3_row.expand()
    assert parent3_row.is_expanded
    assert parent3_row.content.is_displayed
    assert parent3_row.content.read() == row3_expected_content
