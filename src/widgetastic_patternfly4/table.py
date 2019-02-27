import six

from widgetastic.log import create_item_logger
from widgetastic.widget import Table, TableColumn, TableRow, Widget


class HeaderColumn(TableColumn):
    """Represents a cell in the header row."""

    def __locator__(self):
        return self.browser.element(
            "(./td|./th)[{}]".format(self.position + 1),
            parent=self.parent
        )

    @property
    def is_sortable(self):
        return "pf-c-table__sort" in self.browser.classes(self)

    @property
    def sorting_order(self):
        return self.browser.get_attribute("aria-sort", self)

    def sort(self, order="ascending"):
        if order not in ("ascending", "descending"):
            raise ValueError("order should be either 'ascending' or 'descending'")
        while self.sorting_order != order:
            self.click()


class HeaderRow(TableRow):
    Column = HeaderColumn

    def __init__(self, parent, logger=None):
        Widget.__init__(self, parent, logger=logger)

    def __locator__(self):
        return self.browser.element("./thead/tr", parent=self.parent)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.parent)

    def __getitem__(self, item):
        if isinstance(item, six.string_types):
            index = self.table.header_index_mapping[self.table.ensure_normal(item)]
        elif isinstance(item, int):
            index = item
        else:
            raise TypeError('row[] accepts only integers and strings')
        return self.Column(self, index, logger=create_item_logger(self.logger, item))

    def read(self):
        return self.parent.headers


class PatternflyTable(Table):

    HEADERS = './thead/tr/th|./tr/th|./thead/tr/td' + '|' + Table.HEADER_IN_ROWS

    header_row = HeaderRow()

    def sort_by(self, column, order):
        header = self.header_row[column]
        header.sort(order)

    def _toggle_select_all(self, value, column):
        header = self.header_row[column]
        header.fill(value)

    def select_all(self, column=0):
        self._toggle_select_all(True, column)

    def deselect_all(self, column=0):
        self._toggle_select_all(False, column)
