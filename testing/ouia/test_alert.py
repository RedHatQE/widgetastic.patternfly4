import pytest
from widgetastic.widget import View

from widgetastic_patternfly4.ouia import AlertOUIA


ALERT_TYPES = ["success", "danger", "warning", "info"]


@pytest.fixture(params=ALERT_TYPES)
def alert(browser, request):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-alert-ouia']"
        alert = AlertOUIA(request.param)

    view = TestView(browser)
    return view.alert


def test_alert_is_displayed(alert):
    assert alert.is_displayed


def test_alert_title(alert):
    alert_type = alert.type if alert.type != "error" else "danger"
    assert alert.title == f"{alert_type.capitalize()} alert title"
