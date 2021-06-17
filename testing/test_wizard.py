import pytest
from widgetastic.widget import Text
from widgetastic.widget import View

from widgetastic_patternfly4.wizard import TitledContentMixin
from widgetastic_patternfly4.wizard import WizardContentView
from widgetastic_patternfly4.wizard import WizardMixin


TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/wizard"
# FINISHED_VIEW = FinishedWizardView


class StepView(WizardContentView, TitledContentMixin):
    content = Text(locator=".//p")


@pytest.fixture
def wizard(browser, request):
    class TestView(View, WizardMixin):
        WIZARD_STEPS = {
            "First step": StepView,
            "Second step": StepView,
            "Third step": StepView,
            "Fourth step": StepView,
            #            "Review": ReviewWizardView,
        }
        START_BUTTON = "Show Modal"

    return TestView(browser).wizard


def test_wizard_is_displayed(wizard):
    wizard.start()
    assert wizard.is_displayed
