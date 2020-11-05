import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import PatternflyTable

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/table"

SORT = [
    ("Repositories", "ascending", ["a", "one", "p"]),
    ("Repositories", "descending", ["p", "one", "a"]),
    ("Pull requests", "ascending", ["a", "b", "k"]),
    ("Pull requests", "descending", ["k", "b", "a"]),
]


@pytest.mark.parametrize("sample", SORT, ids=lambda sample: "{}-{}".format(sample[0], sample[1]))
def test_sortable_table(browser, sample):
    header, order, expected_result = sample

    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-table-ouia']"
        table = PatternflyTable("Sortable Table")

    view = TestView(browser)
    view.table.sort_by(header, order)
    column = [row[header] for row in view.table.read()]
    assert column == expected_result
