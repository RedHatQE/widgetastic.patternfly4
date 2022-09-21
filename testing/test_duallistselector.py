import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import DualListSelector
from widgetastic_patternfly4 import SearchDualListSelector

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/dual-list-selector"


@pytest.fixture
def view(browser):
    class TestView(View):
        dual_list_selector = DualListSelector(
            locator='.//div[@id="ws-react-c-dual-list-selector-basic"]'
        )
        dual_list_selector_with_search = SearchDualListSelector(
            locator='.//div[@id="ws-react-c-dual-list-selector-basic-with-search"]'
        )

    return TestView(browser)


def test_dual_list_selector_is_displayed(view):
    assert view.dual_list_selector.is_displayed
    assert view.dual_list_selector_with_search.is_displayed


def test_available(view):
    view.dual_list_selector._available.is_displayed()


def test_chosen(view):
    assert view.dual_list_selector._chosen.is_displayed()


def test_get_left_list(view):
    left_list = view.dual_list_selector._left_list
    assert left_list.is_displayed()


def test_get_left_elements(view):
    left_elements = view.dual_list_selector._left_elements
    assert len(left_elements) == 4


def test_get_right_list(view):
    right_list = view.dual_list_selector._right_list
    assert right_list.is_displayed()


def test_get_right_elements(view):
    right_elements = view.dual_list_selector._right_elements
    assert len(right_elements) == 0


def test_get_left_title(view):
    left_title = view.dual_list_selector._left_title
    assert left_title == "Available options"


def test_get_right_title(view):
    right_title = view.dual_list_selector._right_title
    assert right_title == "Chosen options"


def test_get_selected_left_elements(view, request):
    @request.addfinalizer
    def _finalizer():
        view.dual_list_selector.reset_selected()

    view.dual_list_selector.select(["Option 1"])
    selected_left_elements = view.dual_list_selector._selected_left_elements
    assert len(selected_left_elements) == 1


def test_get_selected_right_elements(view, request):
    @request.addfinalizer
    def _finalizer():
        view.dual_list_selector.reset_selected(left_items=False)
        view.dual_list_selector.move_all_items_left()

    view.dual_list_selector.select_and_move(["Option 1"])
    view.dual_list_selector.select(["Option 1"], left_items=False)
    selected_right_elements = view.dual_list_selector._selected_right_elements
    assert len(selected_right_elements) == 1


def test_move_all_items_right_and_left(view):
    view.dual_list_selector.move_all_items_right()
    right_elements = view.dual_list_selector._right_elements
    assert len(right_elements) == 4

    view.dual_list_selector.move_all_items_left()
    left_elements = view.dual_list_selector._left_elements
    assert len(left_elements) == 4


def test_move_selected_items_right(view, request):
    @request.addfinalizer
    def _finalizer():
        view.dual_list_selector.move_all_items_left()

    view.dual_list_selector.select(["Option 1"])
    view.dual_list_selector.move_selected_items_right()
    right_elements = view.dual_list_selector._right_elements
    assert len(right_elements) == 1


def test_move_selected_items_left(view):
    view.dual_list_selector.select_and_move(["Option 1"])

    view.dual_list_selector.select(["Option 1"], left_items=False)
    view.dual_list_selector.move_selected_items_left()
    left_elements = view.dual_list_selector._left_elements
    assert len(left_elements) == 4


def test_read(view):
    data = view.dual_list_selector.read()
    assert len(data["Available options"]) == 4
    assert len(data["Chosen options"]) == 0


def test_reset_selected(view, request):
    @request.addfinalizer
    def _finalizer():
        view.dual_list_selector.move_all_items_left()

    view.dual_list_selector.select(["Option 1"])
    left_elements = view.dual_list_selector._left_elements
    assert left_elements[0].get_attribute("aria-selected") == "true"
    view.dual_list_selector.reset_selected()
    assert left_elements[0].get_attribute("aria-selected") == "false"

    view.dual_list_selector.select_and_move(["Option 2"])
    view.dual_list_selector.select(["Option 2"], left_items=False)
    right_elements = view.dual_list_selector._right_elements
    assert right_elements[0].get_attribute("aria-selected") == "true"
    view.dual_list_selector.reset_selected(left_items=False)
    assert right_elements[0].get_attribute("aria-selected") == "false"


def test_select(view, request):
    @request.addfinalizer
    def _finalizer():
        view.dual_list_selector.reset_selected()

    view.dual_list_selector.select(["Option 1"])
    selected_items = view.dual_list_selector._selected_left_elements
    assert len(selected_items) == 1


def test_select_and_move(view, request):
    @request.addfinalizer
    def _finalizer():
        view.dual_list_selector.move_all_items_left()

    view.dual_list_selector.select_and_move(["Option 2"])
    selected_items = view.dual_list_selector._right_elements
    assert len(selected_items) == 1
    assert selected_items[0].text == "Option 2"


def test_search(view):
    view.dual_list_selector_with_search.search("Option 1")
    items = view.dual_list_selector_with_search._left_elements
    assert len(items) == 1
    assert items[0].text == "Option 1"
