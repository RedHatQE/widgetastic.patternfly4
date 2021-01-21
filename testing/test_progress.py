import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import Progress

TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/progress"
PROGRESS_STATUS_TYPES_WITH_CURRENT_PROGRESS = {
    "success": "100",
    "danger": "33",
    "warning": "90",
    "info": "33",
}


@pytest.fixture(params=PROGRESS_STATUS_TYPES_WITH_CURRENT_PROGRESS.keys())
def progress(browser, request):
    class TestView(View):
        ROOT = ".//main"
        if request.param == "info":
            progress = Progress(locator="(.//div[@class='pf-c-progress'])[1]")
        else:
            progress = Progress(locator=f"(.//div[@class='pf-c-progress pf-m-{request.param}'])[1]")

    return TestView(browser).progress


def test_progress_is_displayed(progress):
    assert progress.is_displayed


def test_progress_status_with_current_progress(progress):
    progress_status_type = progress.status if progress.status != "error" else "danger"
    assert progress_status_type in PROGRESS_STATUS_TYPES_WITH_CURRENT_PROGRESS.keys()
    assert (
        PROGRESS_STATUS_TYPES_WITH_CURRENT_PROGRESS[progress_status_type]
        == progress.current_progress
    )


def test_progress_description(progress):
    assert progress.description == "Title"
