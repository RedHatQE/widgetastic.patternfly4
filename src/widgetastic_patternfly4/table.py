import six

from widgetastic.log import create_item_logger
from widgetastic.widget import Table, TableColumn, TableRow, Text, Widget
from widgetastic.widget.table import resolve_table_widget


class HeaderColumn(TableColumn):
    """Represents a cell in the header row."""

    def __locator__(self):
        return "(./td|./th)[{}]".format(self.position + 1)

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
        return "./thead/tr"

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.parent)

    def __getitem__(self, item):
        if isinstance(item, six.string_types):
            index = self.table.header_index_mapping[self.table.ensure_normal(item)]
        elif isinstance(item, int):
            index = item
        else:
            raise TypeError("row[] accepts only integers and strings")
        return self.Column(self, index, logger=create_item_logger(self.logger, item))

    def read(self):
        return self.parent.headers


class PatternflyTable(Table):
    """Represents the Patternfly table.

    http://patternfly-react.surge.sh/patternfly-4/components/table
    """

    HEADERS = "./thead/tr/th|./tr/th|./thead/tr/td" + "|" + Table.HEADER_IN_ROWS

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


class ExpandableTableRow(TableRow):
    """Represents a row in the table.

    If subclassing and also changing the Column class, do not forget to set the Column to the new
    class.

    Args:
        index: Position of the row in the table.
    """

    ROW = "./tr[1]"
    EXPANDABLE_CONTENT = "./tr[2]/td[2]"

    def __init__(self, parent, index, content_view=None, logger=None):
        Widget.__init__(self, parent, logger=logger)
        # We don't need to adjust index by +1 because anytree Node position will
        # already be '+1' due to presence of 'thead' among the 'tbody' rows
        self.index = index
        content_parent = Text(parent=self, locator=self.EXPANDABLE_CONTENT)
        if content_view:
            self.content = resolve_table_widget(content_parent, content_view)
        else:
            self.content = content_parent

    def __locator__(self):
        # We don't need to adjust index by +1 because anytree Node position will
        # already be '+1' due to presence of 'thead' among the 'tbody' rows
        return self.parent.ROW_AT_INDEX.format(self.index)

    @property
    def is_displayed(self):
        return self.browser.is_displayed(locator=self.ROW)

    @property
    def is_expanded(self):
        return self.browser.is_displayed(locator=self.EXPANDABLE_CONTENT)

    def expand(self):
        if not self.is_expanded:
            self[0].widget.click()
            self.content.wait_displayed()

    def collapse(self):
        if self.is_expanded:
            self[0].widget.click()

    def read(self):
        result = super().read()
        # Remove the column with the "expand" button in it
        if 0 in result and not result[0]:
            del result[0]
        return result


class ExpandableTable(PatternflyTable):
    """
    The patternfly 4 expandable table has the following outline:

    <table>
      <thead>
      <tbody>
        <tr>The row always on display.</tr>
        <tr>The "expandable" content viewed by clicking the arrow button</tr>
      </tbody>
      <tbody>
        <tr>Next row...</tr>
        <tr>Next row's expandable content...</tr>

    Therefore, we modify the behavior of Table here to look for rows based on 'tbody'
    tags instead of 'tr' tags. We use a custom class, ExpandableTableRow, which treats
    the first <tr> tag as a normal table row (if you call row.read(), it will read the
    this row -- also table column widgets will apply to this row, etc. etc.), but it
    will treat the second <tr> tag as a Text widget, or a parent for a custom defined View
    """

    ROWS = "./tbody"
    ROW_RESOLVER_PATH = "/table/tbody"
    ROW_AT_INDEX = "./tbody[{0}]"
    COLUMN_RESOLVER_PATH = "/tr[0]/td"
    COLUMN_AT_POSITION = "./tr[1]/td[{0}]"
    ROW_TAG = "tbody"
    Row = ExpandableTableRow

    def __init__(self, *args, **kwargs):
        """Extend init of Table

        Automatically add the 'expand' button widget as column 0.

        Provide additional kwarg for 'content_view', which is used to pass in a WidgetDescriptor
        to be used as the Widget/View for the expanded content of each row.
        """
        column_widgets = kwargs.get("column_widgets")
        self.content_view = kwargs.pop("content_view", None)
        if column_widgets and 0 not in column_widgets:
            kwargs["column_widgets"][0] = Text('./button[contains(@class, "pf-c-button")]')
        super().__init__(*args, **kwargs)

    def _create_row(self, parent, index, logger=None):
        return self.Row(parent, index, self.content_view, logger)
