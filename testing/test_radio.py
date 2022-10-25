import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import Radio


TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/radio"


class RadioTestView(View):
    controlled_id = Radio(id="radio-controlled")
    uncontrolled_label = Radio(label_text="Uncontrolled radio example")
    description_body = Radio(id="radio-description-body")
    disabled_radio = Radio(id="radio-disabled")
    disabled_checked = Radio(id="radio-disabled-checked")


@pytest.mark.parametrize(
    "test_widget",
    [
        ("controlled_id", dict(radio=False, label="Controlled radio")),
        ("uncontrolled_label", dict(radio=False, label="Uncontrolled radio example")),
        (
            "description_body",
            dict(
                radio=False,
                label="Radio with description and body",
                description="Single-tenant cloud service hosted and managed by Red Hat that offers "
                "high-availability enterprise-grade clusters in a virtual private cloud on "
                "AWS or GCP.",
                body="This is where custom content goes.",
            ),
        ),
    ],
    ids=["id_locator", "label_locator", "with_description"],
)
def test_location(browser, test_widget):
    widget_name, expected_read = test_widget
    view = RadioTestView(browser)
    widget = getattr(view, widget_name)
    assert widget.is_displayed
    assert widget.read() == expected_read
    assert widget.selected is False
    assert widget.fill(True) is True
    assert widget.selected is True


def test_disabled(browser):
    view = RadioTestView(browser)
    assert view.disabled_radio.disabled is True
    assert view.disabled_radio.selected is False
    assert view.disabled_checked.disabled is True
    assert view.disabled_checked.selected is True
