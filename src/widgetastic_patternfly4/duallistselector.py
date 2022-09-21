from widgetastic.widget import GenericLocatorWidget
from widgetastic.widget import TextInput

from .button import Button


class BaseDualListSelector:
    """Represents the Patternfly-4 Dual list selector.

    https://www.patternfly.org/v4/components/dual-list-selector
    """

    AVAILABLE = ".//div[contains(@class, 'pf-m-available')]"
    CHOSEN = ".//div[contains(@class, 'pf-m-chosen')]"

    LIST_ITEMS = ".//div[contains(@class, 'dual-list-selector__menu')]"
    SECTION_TITLE = ".//div[@class='pf-c-dual-list-selector__title-text']"
    ITEMS = ".//li[contains(@class, 'dual-list-selector__list-item')]"
    SELECTED_ITEMS = (
        ".//li[@aria-selected='true' and contains(@class, 'dual-list-selector__list-item')]"
    )
    move_all_right = Button(locator=".//button[@aria-label='Add all']")
    move_selected_right = Button(locator=".//button[@aria-label='Add selected']")
    move_selected_left = Button(locator=".//button[@aria-label='Remove selected']")
    move_all_left = Button(locator=".//button[@aria-label='Remove all']")

    @property
    def _available(self):
        return self.browser.element(self.AVAILABLE, parent=self)

    @property
    def _chosen(self):
        return self.browser.element(self.CHOSEN, parent=self)

    @property
    def _left_list(self):
        return self.browser.element(self.LIST_ITEMS, parent=self._available)

    @property
    def _right_list(self):
        return self.browser.element(self.LIST_ITEMS, parent=self._chosen)

    @property
    def _left_title(self):
        return self.browser.element(self.SECTION_TITLE, parent=self._available).text

    @property
    def _right_title(self):
        return self.browser.element(self.SECTION_TITLE, parent=self._chosen).text

    @property
    def _left_elements(self):
        return self.browser.elements(self.ITEMS, parent=self._left_list)

    @property
    def _right_elements(self):
        return self.browser.elements(self.ITEMS, parent=self._right_list)

    @property
    def _selected_left_elements(self):
        return self.browser.elements(self.SELECTED_ITEMS, parent=self._left_list)

    @property
    def _selected_right_elements(self):
        return self.browser.elements(self.SELECTED_ITEMS, parent=self._right_list)

    def move_all_items_right(self):
        self.move_all_right.click()

    def move_all_items_left(self):
        self.move_all_left.click()

    def move_selected_items_right(self):
        self.move_selected_right.click()

    def move_selected_items_left(self):
        self.move_selected_left.click()

    def read(self, selected_only=False):
        """Read items on left and right sides, if selected_only = True, read only selected items"""
        data = dict()

        if selected_only:
            right_elements = self._selected_right_elements
            left_elements = self._selected_left_elements
        else:
            right_elements = self._right_elements
            left_elements = self._left_elements

        data[self._left_title] = [el.text for el in left_elements]
        data[self._right_title] = [el.text for el in right_elements]
        return data

    def reset_selected(self, left_items=True):
        if left_items:
            _elements = self._left_elements
        else:
            _elements = self._right_elements

        for element in _elements:
            if element.get_attribute("aria-selected") == "true":
                element.click()

    def select(self, items, left_items=True):
        """Select certain items based on text. Defaults to select left_items"""
        if left_items:
            _elements = self._left_elements
        else:
            _elements = self._right_elements

        text_item_map = {self.browser.text(el): el for el in _elements}
        for item in items:
            el = text_item_map.get(item)
            if not el:
                raise ValueError("item not available. select proper one like raise an error")
            self.browser.click(el)

    def select_and_move(self, items, left_items=True):
        """Select and move certain items based on text. Defaults to select
        left_items and move to right"""
        self.select(items, left_items=left_items)

        if left_items:
            self.move_selected_items_right()
        else:
            self.move_selected_items_left()


class DualListSelector(BaseDualListSelector, GenericLocatorWidget):
    pass


class SearchDualListSelector(DualListSelector):
    INPUT = "//input"

    def search(self, value, left_column=True):
        """Fills a Dual list selector with the supplied value depending on column."""
        if left_column:
            text_input_widget = TextInput(self, locator=self.AVAILABLE + self.INPUT)
        else:
            text_input_widget = TextInput(self, locator=self.CHOSEN + self.INPUT)

        text_input_widget.fill(value)
