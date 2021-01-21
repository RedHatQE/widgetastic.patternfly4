from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget


class BaseProgress:
    """Represents the Patternfly Progress

    https://www.patternfly.org/v4/components/progress
    """

    DESCRIPTION = './/div[@class="pf-c-progress__description"]'
    MEASURE = './/span[@class="pf-c-progress__measure"]'
    PROGRESS_BAR = ".//div[@class='pf-c-progress__bar']"
    STATUS_TYPE_MAPPING = {
        "pf-m-warning": "warning",
        "pf-m-success": "success",
        "pf-m-danger": "error",
    }

    @property
    def description(self):
        el = self.browser.element(self.DESCRIPTION)
        return self.browser.text(el)

    @property
    def current_progress(self):
        return self.browser.element(self.PROGRESS_BAR).get_attribute("aria-valuenow")

    @property
    def status(self):
        """Returns the status of the progress, one of warning, success, error or info."""
        for class_ in self.browser.classes(self):
            if class_ in self.STATUS_TYPE_MAPPING:
                return self.STATUS_TYPE_MAPPING[class_]
        else:
            default_alert_type = "info"
            return default_alert_type


class Progress(BaseProgress, Widget):
    ROOT = ParametrizedLocator("{@locator}")

    def __init__(self, parent, locator, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator
