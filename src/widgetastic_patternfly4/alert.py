from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget


class Alert(Widget):
    """Represents alert block.

    http://patternfly-react.surge.sh/patternfly-4/components/alert
    """

    ROOT = ParametrizedLocator("{@locator}")
    TITLE = './/h4[@class="pf-c-alert__title"]'
    DESCRIPTION = './/div[@class="pf-c-alert__description"]'
    ACTION = './/div[@class="pf-c-alert__action"]/*'
    TYPE_MAPPING = {
        "pf-m-warning": "warning",
        "pf-m-success": "success",
        "pf-m-danger": "error",
        "pf-m-info": "info",
    }

    def __init__(self, parent, locator, logger=None):
        super(Alert, self).__init__(parent, logger=logger)
        self.locator = locator

    def read(self):
        return self.body

    @property
    def _raw_title_el(self):
        return self.browser.element(self.TITLE)

    @property
    def title(self):
        trim_text = self.browser.text(self.browser.element("./span", parent=self._raw_title_el))
        return self.browser.text(self._raw_title_el)[len(trim_text):].strip()

    @property
    def body(self):
        el = self.browser.element(self.DESCRIPTION)
        return self.browser.text(el)

    def click_action(self):
        el = self.browser.element(self.ACTION)
        self.browser.click(el)

    @property
    def type(self):
        for class_ in self.browser.classes(self):
            if class_ in self.TYPE_MAPPING:
                return self.TYPE_MAPPING[class_]
        else:
            raise ValueError(
                "Could not find a proper alert type."
                " Available classes: {!r} Alert has: {!r}".format(
                    self.TYPE_MAPPING, self.browser.classes(self)
                )
            )

    def assert_no_error(self):
        if self.type == "error":
            raise AssertionError("assert_no_error: {}".format(self.body))

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.locator)
