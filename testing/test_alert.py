import pytest

from widgetastic_patternfly4 import Alert


ALERT_TYPES = ["success", "danger", "warning", "info"]


@pytest.fixture(params=ALERT_TYPES)
def alert(browser, request):
    return Alert(browser, locator=f".//div[@class='pf-c-alert pf-m-{request.param}'][1]")


def test_alert_is_displayed(alert):
    assert alert.is_displayed


def test_alert_title(alert):
    alert_type = alert.type if alert.type != "error" else "danger"
    assert alert.title == f"{alert_type.capitalize()} alert title"
