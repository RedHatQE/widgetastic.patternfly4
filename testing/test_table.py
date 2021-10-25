import pytest
from widgetastic.widget import Checkbox
from widgetastic.widget import View

from widgetastic_patternfly4 import ColumnNotExpandable
from widgetastic_patternfly4 import CompoundExpandableTable
from widgetastic_patternfly4 import ExpandableTable
from widgetastic_patternfly4 import PatternflyTable
from widgetastic_patternfly4 import RowNotExpandable

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/table"

SORT = [
    (
        "This is a really long table header that goes on for a long time 1.",
        "ascending",
        ["a", "one", "p"],
    ),
    (
        "This is a really long table header that goes on for a long time 1.",
        "descending",
        ["p", "one", "a"],
    ),
    (
        "This is a really long table header that goes on for a long time 3.",
        "ascending",
        ["a", "b", "k"],
    ),
    (
        "This is a really long table header that goes on for a long time 3.",
        "descending",
        ["k", "b", "a"],
    ),
]


@pytest.mark.parametrize("sample", SORT, ids=lambda sample: "{}-{}".format(sample[0], sample[1]))
def test_sortable_table(browser, sample):
    header, order, expected_result = sample
    table = PatternflyTable(
        browser,
        ".//div[@id='ws-react-composable-c-table-composable-sortable--wrapping-headers']/table",
    )
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
        ".//div[@id='ws-react-composable-c-table-composable-selectable-with-checkbox']//table",
        column_widgets={0: Checkbox(locator=".//input")},
    )
    getattr(table, method)()
    for row in table:
        if row.index != 1:  # skip row with disabled checkbox
            assert expected_result == row[0].widget.selected


def test_expandable_table(browser):
    expected_read = [
        {
            "Repositories": "one",
            "Branches": "two",
            "Pull requests": "a",
            "Workspaces": "four",
            "Last commit": "five",
        },
        {
            "Repositories": "parent 1",
            "Branches": "two",
            "Pull requests": "k",
            "Workspaces": "four",
            "Last commit": "five",
        },
        {
            "Repositories": "parent 2",
            "Branches": "two",
            "Pull requests": "b",
            "Workspaces": "four",
            "Last commit": "five",
        },
        {
            "Repositories": "parent 3",
            "Branches": "2",
            "Pull requests": "b",
            "Workspaces": "four",
            "Last commit": "five",
        },
        {
            "Repositories": "parent 4",
            "Branches": "2",
            "Pull requests": "b",
            "Workspaces": "four",
            "Last commit": "five",
        },
        {
            "Repositories": "parent 5",
            "Branches": "2",
            "Pull requests": "b",
            "Workspaces": "four",
            "Last commit": "five",
        },
        {
            "Repositories": "parent 6",
            "Branches": "2",
            "Pull requests": "b",
            "Workspaces": "four",
            "Last commit": "five",
        },
    ]

    row1_expected_content = "single cell"
    row2_expected_content = "single cell - fullWidth"
    row3_expected_content = "single cell - noPadding"

    table = ExpandableTable(
        browser, ".//div[@id='ws-react-composable-c-table-composable-expandable']/table"
    )

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


@pytest.mark.parametrize(
    "use_different_widgets",
    [True, False],
    ids=["diff-widgets-expandable-content", "same-widget-expandable-content"],
)
def test_compound_expandable_table(browser, use_different_widgets):
    table_read = [
        {
            "Repositories": "siemur/test-space",
            "Branches": "10",
            "Pull requests": "4",
            "Workspaces": "4",
            "Last commit": "20 minutes",
            5: "Open in Github",
        },
        {
            "Repositories": "siemur/test-space",
            "Branches": "3",
            "Pull requests": "4",
            "Workspaces": "2",
            "Last commit": "10 minutes",
            5: "Open in Github",
        },
    ]

    row0_branches_read = {
        "table": [
            {
                "Repositories": "parent-0",
                "Branches": "compound-1",
                "Pull requests": "three",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "a",
                "Branches": "two",
                "Pull requests": "k",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "p",
                "Branches": "two",
                "Pull requests": "b",
                "Workspaces": "four",
                "Last Commit": "five",
            },
        ]
    }
    row0_pull_requests_read = {
        "table": [
            {
                "Repositories": "parent-0",
                "Branches": "compound-2",
                "Pull requests": "three",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "a",
                "Branches": "two",
                "Pull requests": "k",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "p",
                "Branches": "two",
                "Pull requests": "b",
                "Workspaces": "four",
                "Last Commit": "five",
            },
        ]
    }
    row0_workspaces_read = {
        "table": [
            {
                "Repositories": "parent-0",
                "Branches": "compound-3",
                "Pull requests": "three",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "a",
                "Branches": "two",
                "Pull requests": "k",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "p",
                "Branches": "two",
                "Pull requests": "b",
                "Workspaces": "four",
                "Last Commit": "five",
            },
        ]
    }
    row1_branches_read = {
        "table": [
            {
                "Repositories": "parent-1",
                "Branches": "compound-1",
                "Pull requests": "three",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "a",
                "Branches": "two",
                "Pull requests": "k",
                "Workspaces": "four",
                "Last Commit": "five",
            },
            {
                "Repositories": "p",
                "Branches": "two",
                "Pull requests": "b",
                "Workspaces": "four",
                "Last Commit": "five",
            },
        ]
    }
    if use_different_widgets:
        # for the example table all the expanded tables are the same, besides the different id
        # that we use in the locator
        class _Branches(View):
            table = PatternflyTable(locator=".//table[contains(@id, '_1')]")

        class _PullRequests(View):
            table = PatternflyTable(locator=".//table[contains(@id, '_2')]")

        class _Workspaces(View):
            table = PatternflyTable(locator=".//table[contains(@id, '_3')]")

        content_view = {1: _Branches(), 2: _PullRequests(), 3: _Workspaces()}
    else:
        # use the same content_view for all the tables
        class _ContentView(View):
            """ View for the nested table(s) in the expandable columns."""

            table = PatternflyTable(locator=".//table[@aria-label='Sortable Table']")

        content_view = _ContentView()

    table = CompoundExpandableTable(
        browser, ".//table[@aria-label='Compound expandable table']", content_view=content_view
    )

    assert table.read() == table_read

    # Make sure that the appropriate columns are expandable
    for row in table.rows():
        assert not row.repositories.is_expandable
        assert not row.last_commit.is_expandable
        assert row.branches.is_expandable
        assert row.pull_requests.is_expandable
        assert row.workspaces.is_expandable

    # first column is not an expandable column
    with pytest.raises(ColumnNotExpandable):
        table[0][0].expand()
    with pytest.raises(ColumnNotExpandable):
        table[1][0].expand()

    # first row
    row0 = table[0]
    row0.branches.expand()
    assert row0.branches.is_expanded
    assert row0.branches.content.read() == row0_branches_read
    row0.branches.collapse()
    assert not row0.branches.is_expanded

    row0.pull_requests.expand()
    assert row0.pull_requests.is_expanded
    assert row0.pull_requests.content.read() == row0_pull_requests_read
    row0.pull_requests.collapse()
    assert not row0.pull_requests.is_expanded

    row0.workspaces.expand()
    assert row0.workspaces.is_expanded
    assert row0.workspaces.content.read() == row0_workspaces_read
    row0.workspaces.collapse()
    assert not row0.workspaces.is_expanded

    # second row, just test the first expandable column
    row1 = table[1]
    row1.branches.expand()
    assert row1.branches.is_expanded
    assert row1.branches.content.read() == row1_branches_read
    row1.branches.collapse()
    assert not row1.branches.is_expanded
