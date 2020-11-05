import re

import pytest
from widgetastic.exceptions import WidgetOperationFailed
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import BreadCrumb

TESTING_PAGE_URL = (
    "https://patternfly-docs-ouia.netlify.app/documentation/react/components/breadcrumb"  # noqa
)


def test_breadcrumb(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-breadcrumb-ouia']"
        breadcrumb = BreadCrumb("basic")

    view = TestView(browser)
    assert view.breadcrumb.is_displayed
    assert len(view.breadcrumb.locations) == 4
    assert view.breadcrumb.locations[0].lower() == "section home"
    assert view.breadcrumb.read().lower() == "section landing"
    view.breadcrumb.click_location(view.breadcrumb.locations[0])
    view.breadcrumb.click_location("title", partial=True)

    failing_location = "definitely not in the example page"

    # exception + message on full match
    exception_match = re.escape(
        f'Breadcrumb location "{failing_location}" '
        f"not found within locations: {view.breadcrumb.locations}"
    )
    with pytest.raises(WidgetOperationFailed, match=exception_match):
        view.breadcrumb.click_location(failing_location)

    # exception + message on partial match
    exception_match = re.escape(
        f'Breadcrumb location "{failing_location}" '
        "not found with partial match "
        f"within locations: {view.breadcrumb.locations}"
    )
    with pytest.raises(WidgetOperationFailed, match=exception_match):
        view.breadcrumb.click_location(failing_location, partial=True)
