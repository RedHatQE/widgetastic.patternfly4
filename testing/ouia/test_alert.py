import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import Alert

TESTING_PAGE_URL = "https://patternfly-docs-ouia.netlify.app/documentation/react/components/alert"

ALERT_TYPES = ["success", "danger", "warning", "info"]


@pytest.fixture(params=ALERT_TYPES)
def alert(browser, request):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-alert-ouia']"
        alert = Alert(request.param)

    view = TestView(browser)
    return view.alert


def test_alert_is_displayed(alert):
    assert alert.is_displayed


def test_alert_title(alert):
    alert_type = alert.type if alert.type != "error" else "danger"
    assert alert.title == f"{alert_type.capitalize()} alert title"
