import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import ClipboardCopy

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/clipboard-copy"


@pytest.fixture
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-clipboard-copy-basic']"
        clipboardEditable = ClipboardCopy(
            locator="//div[@id='ws-react-c-clipboard-copy-basic']/div[1]"
        )
        clipboardReadOnly = ClipboardCopy(
            locator="//div[@id='ws-react-c-clipboard-copy-read-only']/div[1]"
        )
        clipboardInline = ClipboardCopy(
            locator="//div[@id='ws-react-c-clipboard-copy-inline-compact']/div[1]"
        )

    return TestView(browser)


def test_clipboardcopy_displayed(view):
    assert view.clipboardEditable.is_displayed


def test_clipboardcopy_is_inline(view):
    assert view.clipboardEditable.is_inline is False
    assert view.clipboardInline.is_inline


def test_clipboardcopy_is_editable(view):
    assert view.clipboardEditable.is_editable


def test_clipboardcopy_is_read_only(view):
    assert view.clipboardReadOnly.is_editable is False
    assert view.clipboardInline.is_editable is False


def test_clipboardcopy_text(view):
    assert view.clipboardEditable.read() == "This is editable"

    assert view.clipboardEditable.fill("Test")
    assert view.clipboardEditable.read() == "Test"

    assert view.clipboardReadOnly.read() == "This is read-only"

    assert view.clipboardInline.read() == "2.3.4-2-redhat"


def test_clipboardcopy_copy(view):
    assert view.clipboardEditable.button.is_displayed
    assert view.clipboardReadOnly.button.is_displayed
    assert view.clipboardInline.button.is_displayed
    view.clipboardReadOnly.copy()
    view.clipboardEditable.copy()
    view.clipboardInline.copy()
