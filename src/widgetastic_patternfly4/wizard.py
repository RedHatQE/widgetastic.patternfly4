from widgetastic.widget import Text
from widgetastic.widget import View
from widgetastic.widget import Widget
from widgetastic.widget import WTMixin

from widgetastic_patternfly4 import Button


class TitledContentMixin(WTMixin):

    TITLE_LOCATOR = ".//h1"

    @property
    def title(self):
        return self._get_value_if_displayed(self.TITLE_LOCATOR)

    @property
    def subtitle(self):

        SUBTITLE_LOCATOR = f"{self.TITLE_LOCATOR}//following-sibling::*"
        return self._get_value_if_displayed(SUBTITLE_LOCATOR)

    def _get_value_if_displayed(self, locator):

        widget = Text(self, locator)

        if widget.is_displayed:
            return widget.text
        else:
            self.logger.warning(
                "widget with locator '%s' not found, returning empty string value", locator
            )
            return ""


class WizardSteps(View):

    ROOT = ".//nav[@class='pf-c-wizard__nav']"
    STEPS_LOCATOR = ".//li[@class = 'pf-c-wizard__nav-item']"
    CURRENT_STEP = f"{STEPS_LOCATOR}/button[@aria-current='page']"

    @property
    def steps(self):
        return [self.browser.text(elem) for elem in self.browser.elements(self.STEPS_LOCATOR)]

    @property
    def active_step(self):
        return self.browser.element(self.CURRENT_STEP).text

    def select_step(self, step_name):
        button_locator = self.STEPS_LOCATOR + f'/button[text()="{step_name}"]'
        self.browser.element(button_locator).click()


class WizardHeaderView(View, TitledContentMixin):

    ROOT = ".//div[@class='pf-c-wizard__header']"
    TITLE_LOCATOR = ".//h2"
    CLOSE_LOCATOR = ".//button[@aria-label='Close']"
    close_button = Button(locator=CLOSE_LOCATOR)


class WizardFooterView(View):

    ROOT = ".//footer[@class='pf-c-wizard__footer']"

    next_button = Button("Next")
    back_button = Button("Back")
    cancel_button = Button("Cancel")
    finish_button = Button("Finish")

    @property
    def is_displayed(self):
        return (
            (self.next_button.is_displayed or self.finish_button.is_displayed)
            and self.back_button.is_displayed
            and self.cancel_button.is_displayed
        )


class WizardContentView(View):

    ROOT = ".//main[@class='pf-c-wizard__main']"

    def is_displayed(self):
        raise NotImplementedError


class WizardMainView(View):

    ROOT = ".//*[@class='pf-c-wizard']"
    _content_views = {}

    steps_view = View.nested(WizardSteps)
    header_view = View.nested(WizardHeaderView)
    footer_view = View.nested(WizardFooterView)
    finished_view = None

    # TODO: Add title and subtitle

    def __init__(self, parent, content_views=None, finished_view=None, logger=None):
        content_views = content_views or {}
        finished_view = finished_view or {}

        super(WizardMainView, self).__init__(parent, logger=logger)

        self._content_views = {
            step_name: content_views[step_name](self) for step_name in content_views
        }

        if finished_view:
            self.finished_view = finished_view

    def cancel(self):
        self.footer_view.cancel_button.click()

    # TODO: Buttons should be checked if disabled
    #  (i.e., some views require some actions before continuing)
    def next(self):
        self.footer_view.next_button.click()

    def back(self):
        self.footer_view.back_button.click()

    def finish(self):
        self.footer_view.finish_button.click()

    def step_view(self, step):
        return self._content_views[step]

    def _on_finished_step(self):
        return not self.active_step

    @property
    def current_view(self):
        if self.active_step:
            return self.step_view(self.active_step)
        elif self._on_finished_step():
            return self.finished_view
        else:
            self.logger.info("The wizard is not displayed, cannot retrieve any view")
            return None

    @property
    def active_step(self):
        if self.steps_view.is_displayed:
            return self.steps_view.active_step
        else:
            return None

    def select_step(self, step_name):
        if self.steps_view.is_displayed and step_name in self.steps:
            if self.active_step != step_name:
                self.steps_view.select_step(step_name)
        else:
            raise

    @property
    def steps(self):
        if self.steps_view.is_displayed:
            return self.steps_view.steps
        else:
            return []

    @property
    def is_displayed(self):

        if self._on_finished_step():
            return self.header_view.is_displayed
        else:
            return (
                self.header_view.is_displayed
                and self.steps_view.is_displayed
                and self.footer_view.is_displayed
            )


class Wizard(Widget):

    _main_view = None
    _views = {}

    def __init__(
        self, parent, start_widget, step_view_config=None, finished_view_config=None, logger=None
    ):
        step_view_config = step_view_config or {}
        super(Wizard, self).__init__(parent, logger=logger)
        self._main_view = WizardMainView(self.browser, step_view_config, finished_view_config)
        self._start_widget = start_widget

    @property
    def title(self):
        return self._main_view.header_view.title

    @property
    def subtitle(self):
        return self._main_view.header_view.subtitle

    @property
    def steps(self):
        return self._main_view.steps

    @property
    def is_displayed(self):
        return self._main_view.is_displayed

    @property
    def active_step(self):
        return self._main_view.active_step

    def select_step(self, step_name):
        self._main_view.select_step(step_name)

    def _current_view(self):
        return self._main_view.current_view

    @property
    def view(self):
        return self._current_view()

    def start(self):
        self._start_widget.click()

    def _click_button(self, button_type="next", wait_for_view=True):

        # TODO: better create enum?
        if button_type == "next":
            button = self._main_view.footer_view.next_button
        else:
            button = self._main_view.footer_view.finish_button

        if button.is_displayed and button.is_enabled:
            button.click()
        else:
            raise ValueError("No button type %s found or enabled", button_type)

        if wait_for_view:
            self.view.wait_displayed(delay=1)

    def finish(self, wait_for_view=True):
        self._click_button("finish", wait_for_view=wait_for_view)

    def next(self, wait_for_view=True):
        self._click_button("next", wait_for_view=wait_for_view)

    # TODO: Wrap back, cancel, close buttons with wait wrappers like next, finish buttons.
    # TODO: Probably remove finish(), next() helper methods from wizard.
    def back(self):
        self._main_view.back()

    def cancel(self):
        self._main_view.cancel()

    def close(self):
        self._main_view.header_view.close_button.click()


class WizardMixin(WTMixin):

    START_BUTTON = None
    STEPS = None
    FINISHED_VIEW = None

    @property
    def wizard(self):

        start_wizard_widget = (
            self.START_BUTTON
            if isinstance(self.START_BUTTON, Widget)
            else Button(self.browser, self.START_BUTTON)
        )

        wizard = Wizard(self.browser, start_wizard_widget, self.STEPS, self.FINISHED_VIEW)

        return wizard
