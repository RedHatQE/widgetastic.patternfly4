import pytest
from widgetastic.widget import Text
from widgetastic.widget import View

from widgetastic_patternfly4.button import Button
from widgetastic_patternfly4.wizard import TitledContentMixin
from widgetastic_patternfly4.wizard import WizardContentView
from widgetastic_patternfly4.wizard import WizardMixin


TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/wizard"


class StepView(WizardContentView, TitledContentMixin):
    content = Text(locator=".//p")


#
# class ReviewView(StepView):
#     pass


@pytest.fixture
def wizard(browser):
    class TestView(View, WizardMixin):
        START_BUTTON = Button(locator=".//button[contains(text(), 'Show Modal')]")
        STEPS = {
            "First step": StepView,
            "Second step": StepView,
            "Third step": StepView,
            "Fourth step": StepView,
            "Review": StepView,
        }
        FINISH_BUTTON = "Finish"
        wizard = WizardMixin().wizard

    return TestView(browser).wizard


def test_wizard_is_displayed(wizard):
    wizard.start()
    assert wizard.is_displayed
    wizard.close()
    assert not wizard.is_displayed


def test_wizard_navigation_until_finish(wizard):
    wizard.start()
    assert wizard.view.content.text == "Step 1 content"
    wizard.next()
    assert wizard.view.content.text == "Step 2 content"
    wizard.next()
    assert wizard.view.content.text == "Step 3 content"
    wizard.next()
    assert wizard.view.content.text == "Step 4 content"
    wizard.next()
    assert wizard.view.content.text == "Review step content"
    wizard.finish()


def test_wizard_back_and_cancel(wizard):
    wizard.start()
