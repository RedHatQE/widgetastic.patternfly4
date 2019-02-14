import pytest
from widgetastic_patternfly4 import Alert


ALERT_TYPES = ["success", "danger", "warning", "info"]


@pytest.fixture(params=ALERT_TYPES)
def alert(browser, request):
    return Alert(browser, "(.//div[@class='pf-c-alert pf-m-{}'])[1]".format(request.param))


def test_alert_is_displayed(alert):
    assert alert.is_displayed


def test_alert_title(alert):
    alert_type = alert.type if alert.type != "error" else "danger"
    assert alert.title == "{} alert title".format(alert_type.capitalize())


def test_alert_body(alert):
    alert_type = alert.type if alert.type != "error" else "danger"
    assert alert.body == ("{} alert description."
                          " This is a link.".format(alert_type.capitalize()))
