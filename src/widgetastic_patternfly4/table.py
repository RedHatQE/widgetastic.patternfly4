import six
from selenium.common.exceptions import NoSuchElementException
from widgetastic.log import create_item_logger
from widgetastic.widget import Table
from widgetastic.widget import TableColumn
from widgetastic.widget import TableRow
from widgetastic.widget import Text
from widgetastic.widget import Widget
from widgetastic.widget.table import resolve_table_widget


class HeaderColumn(TableColumn):
    """Represents a cell in the header row."""

    def __locator__(self):
        return "(./td|./th)[{}]".format(self.position + 1)

    @property
    def is_sortable(self):
        """Returns true of the column is sortable."""
        return "pf-c-table__sort" in self.browser.classes(self)

    @property
    def sorting_order(self):
        """Returns current sorting order as a string."""
        return self.browser.get_attribute("aria-sort", self)

    def sort(self, order="ascending"):
        """Sorts the column according to the supplied "ascending" or "descending"."""
        if order not in ("ascending", "descending"):
            raise ValueError("order should be either 'ascending' or 'descending'")
        for _ in range(10):
            if self.sorting_order == order:
                break
            self.click()
        else:
            raise AssertionError(f"Could not set sorting order to `{order}` after 10 tries.")


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
        """Returns the values of the headers of the HeaderRow object."""
        return self.parent.headers


class PatternflyTableRow(TableRow):
    """
    Extends TableRow to support having a 'th' tag within the row
    """

    HEADER_IN_ROW = "./th[1]"
    TABLE_COLUMN_CLS = TableColumn

    @property
    def has_row_header(self):
        """Returns a boolean detailing if the Table Row has a header."""
        return len(self.browser.elements(self.HEADER_IN_ROW)) > 0

    def __getitem__(self, item):
        if isinstance(item, six.string_types):
            index = self.table.header_index_mapping[self.table.ensure_normal(item)]
        elif isinstance(item, int):
            index = item
        else:
            raise TypeError("row[] accepts only integers and strings")

        # We need to do adjustments if a <th> tag exists inside the row...
        # Typically the layout is: <td>, <th>, <td>, <td>, <td>, and so on...
        if self.has_row_header:
            if index == 1:
                # We assume the header entry always sits at position 1. Return a TableColumn for it.
                # Pass position '0' since the Column __locator__ uses 'position + 1'
                return self.TABLE_COLUMN_CLS(self, 0, logger=create_item_logger(self.logger, item))

            if index > 1:
                # Adjust the index for td objects that exist beyond the th so xpath is valid
                index = index - 1
        # After adjusting the index, call the original __getitem__ to get our TableColumn item
        return super(PatternflyTableRow, self).__getitem__(index)


class BasePatternflyTable:
    """Represents the Patternfly table.

    https://www.patternfly.org/v4/documentation/react/components/table
    """

    ROWS = "./tbody/tr[./td]"
    HEADERS = "./thead/tr/th|./tr/th|./thead/tr/td"

    Row = PatternflyTableRow

    header_row = HeaderRow()

    @property
    def _is_header_in_body(self):
        """Override this to return False.

        Some PF4 tables have a 'header cell' in the row, which is a th in the row, this will
        cause Table._is_header_in_body to incorrectly return 'True'
        """
        return False

    def sort_by(self, column, order):
        """Sets the sort order for the supplied column by name, and "ascending/descending"."""
        header = self.header_row[column]
        header.sort(order)

    def _toggle_select_all(self, value, column):
        header = self.header_row[column]
        header.fill(value)

    def select_all(self, column=0):
        """Selects all the rows."""
        self._toggle_select_all(True, column)

    def deselect_all(self, column=0):
        """Deselects all the rows."""
        self._toggle_select_all(False, column)


class PatternflyTable(BasePatternflyTable, Table):
    pass


class ExpandableTableHeaderColumn(TableColumn):
    """
    Used for special cases where a <th> appears as a column in ExpandableTable.
    """

    def __locator__(self):
        """Override the locator to look inside the first 'tr' within the tbody"""
        return "./tr[1]/th[{}]".format(self.position + 1)


class RowNotExpandable(Exception):
    def __init__(self, row):
        self.row = row

    def __str__(self):
        return "Row is not expandable: {}".format(repr(self.row))


class ColumnNotExpandable(Exception):
    def __init__(self, column):
        self.column = column

    def __str__(self):
        return "Column is not expandable: {}".format(repr(self.column))


class ExpandableTableRow(PatternflyTableRow):
    """Represents a row in the table.

    If subclassing and also changing the Column class, do not forget to set the Column to the new
    class.

    Args:
        index: Position of the row in the table.
    """

    ROW = "./tr[1]"
    EXPANDABLE_CONTENT = "./tr[2]"

    # Override these values inherited from PatternflyTableRow...
    HEADER_IN_ROW = "./tr[1]/th[1]"
    TABLE_COLUMN_CLS = ExpandableTableHeaderColumn

    def __init__(self, parent, index, content_view=None, logger=None):
        super(ExpandableTableRow, self).__init__(parent, index, logger=logger)

        content_parent = Text(parent=self, locator=self.EXPANDABLE_CONTENT)
        if content_view:
            self.content = resolve_table_widget(content_parent, content_view)
        else:
            self.content = content_parent

    @property
    def is_displayed(self):
        """Returns a boolean detailing if the Table Row is displayed."""
        return self.browser.is_displayed(locator=self.ROW)

    @property
    def is_expandable(self):
        """Returns a boolean detailing if the table row is expandable."""
        return self[0].widget.is_displayed

    def _check_expandable(self):
        if not self.is_expandable:
            raise RowNotExpandable(self)

    @property
    def is_expanded(self):
        """Returns a boolean detailing if the table row has been expanded."""
        self._check_expandable()
        return self.browser.is_displayed(locator=self.EXPANDABLE_CONTENT)

    def expand(self):
        """Expands the table row."""
        self._check_expandable()
        if not self.is_expanded:
            self[0].widget.click()
            self.content.wait_displayed()

    def collapse(self):
        """Collapses the table row."""
        self._check_expandable()
        if self.is_expanded:
            self[0].widget.click()

    def read(self):
        """Returns a text representation of the table row."""
        result = super(ExpandableTableRow, self).read()
        # Remove the column with the "expand" button in it
        if 0 in result and not result[0]:
            del result[0]
        return result


class BaseExpandableTable:
    """
    The patternfly 4 expandable table has the following outline:

    .. code-block:: html

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
    HEADERS = "./thead/tr/th|./thead/tr/td"
    Row = ExpandableTableRow

    def __init__(self, *args, **kwargs):
        """Extend init of Table

        Automatically add the 'expand' button widget as column 0.

        Provide additional kwarg for 'content_view', which is used to pass in a WidgetDescriptor
        to be used as the Widget/View for the expanded content of each row.
        """
        column_widgets = kwargs.get("column_widgets")
        self.content_view = kwargs.pop("content_view", None)

        col_widget = Text('./button[contains(@class, "pf-c-button")]')
        if column_widgets and 0 not in column_widgets:
            # Do not override column 0 if the user defined it during init
            kwargs["column_widgets"][0] = col_widget
        elif not column_widgets:
            kwargs["column_widgets"] = {0: col_widget}

        super().__init__(*args, **kwargs)

    def _create_row(self, parent, index, logger=None):
        return self.Row(parent, index, self.content_view, logger)


class ExpandableTable(BaseExpandableTable, PatternflyTable):
    pass


class ExpandableColumn(TableColumn):
    EXPAND_LOCATOR = "./button"

    def __init__(self, parent, position, content_view=None, absolute_position=None, logger=None):
        super(ExpandableColumn, self).__init__(parent, position, absolute_position, logger=logger)

        expandable_content = f"./tr[{position + 1}]"
        content_parent = Text(parent=self.row, locator=expandable_content)
        if content_view:
            self.content = resolve_table_widget(content_parent, content_view)
        else:
            self.content = content_parent

    def __locator__(self):
        """Override the locator to look inside the first 'tr' within the tbody"""
        if self.position == 0:
            # we assume the th column is in the first position
            return "./tr[1]/th[{}]".format(self.position + 1)
        else:
            return "./tr[1]/td[{}]".format(self.position)

    @property
    def is_expandable(self):
        """ To check to see if this column is expandable, check to see if a button is in it."""
        try:
            self.browser.element(self.EXPAND_LOCATOR)
        except NoSuchElementException:
            return False
        return True

    def _check_expandable(self):
        if not self.is_expandable:
            raise ColumnNotExpandable(self)

    @property
    def widget(self):
        # TODO: make this configurable?
        if self.is_expandable:
            return Text(locator=self.EXPAND_LOCATOR, parent=self)
        else:
            return None

    @property
    def is_expanded(self):
        self._check_expandable()
        return self.browser.get_attribute("aria-expanded", self.widget).lower()[0] in [
            "1",
            "t",
            "y",
        ]

    def expand(self):
        """Expands the table column."""
        self._check_expandable()
        if not self.is_expanded:
            self.widget.click()
            self.content.wait_displayed()

    def collapse(self):
        """Collapses the table column."""
        self._check_expandable()
        if self.is_expanded:
            self.widget.click()


class CompoundExpandableRow(PatternflyTableRow):
    TABLE_COLUMN_CLS = ExpandableColumn
    HEADER_IN_ROW = "./tr[1]/th[1]"
    # these are the columns that allow for expansion
    EXPANDABLE_COLUMNS = "./tr[1]/td[contains(@class, 'compound-expansion')]"
    Column = ExpandableColumn

    def __getitem__(self, item):
        if isinstance(item, six.string_types):
            index = self.table.header_index_mapping[self.table.ensure_normal(item)]
        elif isinstance(item, int):
            index = item
        else:
            raise TypeError("row[] accepts only integers and strings")

        # Typically for this widget the layout is: <th>, <td>, <td>, <td>, and so on...
        if self.has_row_header:
            return self.Column(
                self, index, self.table.content_view, logger=create_item_logger(self.logger, item)
            )

        return super(PatternflyTableRow, self).__getitem__(index)


class CompoundExpandableTable(PatternflyTable):
    """
    This widget is similar to the ExpandableTable, only that it can have any number of
    expandable rows, and the expandable column is not necessarily in the first position.

    https://www.patternfly.org/v4/documentation/react/components/table#
    """

    ROWS = "./tbody"
    ROW_RESOLVER_PATH = "/table/tbody"
    ROW_AT_INDEX = "./tbody[{0}]"
    COLUMN_RESOLVER_PATH = "/tr[0]/td"
    COLUMN_AT_POSITION = "./tr[1]/td[{0}]"
    ROW_TAG = "tbody"
    HEADERS = "./thead/tr/th|./thead/tr/td"

    Row = CompoundExpandableRow

    def __init__(self, *args, **kwargs):
        """Extend init of Table

        Automatically add the 'expand' button widget as column 0.

        Provide additional kwarg for 'content_view', which is used to pass in a WidgetDescriptor
        to be used as the Widget/View for the expanded content of each column.
        """
        self.content_view = kwargs.pop("content_view", None)
        super(CompoundExpandableTable, self).__init__(*args, **kwargs)

    def _create_column(self, parent, position, absolute_position=None, logger=None):
        """Override this if you wish to change column behavior in a child class."""
        return self.Row.Column(parent, position, self.content_view, absolute_position, logger)
