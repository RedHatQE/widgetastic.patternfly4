from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget


class BaseAlert:
    """Represents alert block.

    https://www.patternfly.org/v4/documentation/react/components/alert
    """

    TITLE = './/h4[@class="pf-c-alert__title"]'
    DESCRIPTION = './/div[@class="pf-c-alert__description"]'
    ACTION = './/div[contains(@class, "pf-c-alert__action")]'
    TYPE_MAPPING = {
        "pf-m-warning": "warning",
        "pf-m-success": "success",
        "pf-m-danger": "error",
        "pf-m-info": "info",
    }

    def read(self):
        """Returns the text of the body of the alert as a string."""
        return self.body

    @property
    def _raw_title_el(self):
        return self.browser.element(self.TITLE)

    @property
    def _raw_description_el(self):
        return self.browser.element(self.DESCRIPTION)

    @property
    def title(self):
        """Returns the title text of the alert as a string."""
        trim_text = self.browser.text(self.browser.element("./span", parent=self._raw_title_el))
        return self.browser.text(self._raw_title_el)[len(trim_text) :].strip()

    @property
    def body(self):
        """Returns the text of the body of the alert as a string."""
        el = self.browser.element(self.DESCRIPTION)
        return self.browser.text(el)

    def click_action(self):
        """Clicks the defined action button of the alert."""
        el = self.browser.element(self.ACTION)
        self.browser.click(el)

    def click_link(self):
        el = self.browser.element("./a", parent=self._raw_description_el)
        self.browser.click(el)

    @property
    def type(self):
        """Returns the type of the alert, one of warning, success, error or info."""
        for class_ in self.browser.classes(self):
            if class_ in self.TYPE_MAPPING:
                return self.TYPE_MAPPING[class_]
        else:
            raise ValueError(
                "Could not find a proper alert type."
                f"\nAvailable classes: {self.TYPE_MAPPING!r} "
                f"\nAlert has: {self.browser.classes(self)!r}"
            )

    def assert_no_error(self):
        """Asserts that the warning is not of the error type."""
        if self.type == "error":
            raise AssertionError(f"assert_no_error: {self.body}")

    def __repr__(self):
        return f"{type(self).__name__}({self.locator!r})"


class Alert(BaseAlert, Widget):
    ROOT = ParametrizedLocator("{@locator}")

    def __init__(self, parent, locator, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator
