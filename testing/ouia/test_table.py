import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import PatternflyTableOUIA


SORT = [
    ("Repositories", "ascending", ["a", "one", "p"]),
    ("Repositories", "descending", ["p", "one", "a"]),
    ("Pull requests", "ascending", ["a", "b", "k"]),
    ("Pull requests", "descending", ["k", "b", "a"]),
]


class TestView(View):
    ROOT = ".//div[@id='ws-react-c-table-ouia']"
    table = PatternflyTableOUIA("Sortable Table")


@pytest.mark.parametrize("sample", SORT, ids=lambda sample: "{}-{}".format(sample[0], sample[1]))
def test_sortable_table(browser, sample):
    header, order, expected_result = sample
    view = TestView(browser)
    view.table.sort_by(header, order)
    column = [row[header] for row in view.table.read()]
    assert column == expected_result
