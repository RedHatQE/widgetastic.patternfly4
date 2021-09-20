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


class ReviewView(StepView):
    pass


@pytest.fixture
def view(browser):
    class TestView(View, WizardMixin):
        start_wizard_button = Button("Show Modal")
        STEPS = {
            "First step": StepView,
            "Second step": StepView,
            "Third step": StepView,
            "Fourth step": StepView,
            "Review": ReviewView,
        }
        FOOTER_NEXT_BUTTON = Button(
            locator=".//div[@data-ouia-component-type='PF4/ModalContent']"
            "//button[contains(text(), 'Next')]"
        )
        FOOTER_BACK_BUTTON = Button(
            locator=".//div[@data-ouia-component-type='PF4/ModalContent']"
            "//button[contains(text(), 'Back')]"
        )
        FOOTER_CANCEL_BUTTON = Button(
            locator=".//div[@data-ouia-component-type='PF4/ModalContent']"
            "//button[contains(text(), 'Cancel')]"
        )
        FOOTER_FINISH_BUTTON = Button(
            locator=".//div[@data-ouia-component-type='PF4/ModalContent']"
            "//button[contains(text(), 'Finish')]"
        )

    return TestView(browser)


def test_wizard_is_displayed(view):
    wizard = view.wizard
    view.start_wizard_button.click()
    wizard.wait_displayed()
    assert wizard.title == "Wizard in modal"
    assert wizard.subtitle == "Simple Wizard Description"
    assert wizard.steps == ["First step", "Second step", "Third step", "Fourth step", "Review"]
    wizard.close()
    view.wait_displayed()


def test_wizard_navigation_until_finish(view, request):
    @request.addfinalizer
    def finalizer():
        view.browser.refresh()

    wizard = view.wizard
    view.start_wizard_button.click()
    assert wizard.active_step == "First step"
    assert wizard.view.content.text == "Step 1 content"
    wizard.next()
    assert wizard.active_step == "Second step"
    assert wizard.view.content.text == "Step 2 content"
    wizard.next()
    assert wizard.active_step == "Third step"
    assert wizard.view.content.text == "Step 3 content"
    wizard.next()
    assert wizard.active_step == "Fourth step"
    assert wizard.view.content.text == "Step 4 content"
    wizard.next()
    assert wizard.active_step == "Review"
    assert wizard.view.content.text == "Review step content"
    wizard.finish()
    view.wait_displayed()


def test_wizard_back_and_cancel(view):
    wizard = view.wizard
    view.start_wizard_button.click()
    wizard.next()
    wizard.back()
    assert wizard.active_step == "First step"
    assert wizard.view.content.text == "Step 1 content"
    wizard.cancel()
    assert view.wait_displayed()


def test_wizard_select_step(view, request):
    wizard = view.wizard
    view.start_wizard_button.click()

    @request.addfinalizer
    def finalizer():
        wizard.close()
        view.browser.refresh()

    wizard.select_step("Third step")
    assert wizard.active_step == "Third step"
    assert wizard.view.content.text == "Step 3 content"
