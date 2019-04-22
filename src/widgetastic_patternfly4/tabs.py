from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import View


class Tab(View):
    """Represents the Patternfly Tab widget.

    Selects itself automatically when any child widget gets accessed, ensuring that the widget is
    visible.

    http://patternfly-react.surge.sh/patternfly-4/components/tabs
    """

    # The text on the tab. Can be omitted if it is the same as the tab class name capitalized
    TAB_NAME = None

    # Locator of the Tab selector
    TAB_LOCATOR = ParametrizedLocator(
        './/div[contains(@class, "pf-c-tabs")]/ul'
        "/li[button[normalize-space(.)={@tab_name|quote}]]"
    )

    ROOT = ParametrizedLocator(
        ".//section[@aria-labelledby=string("
        "preceding-sibling::div/ul/li/button[normalize-space(.)={@tab_name|quote}]/@id)]"
    )

    @property
    def tab_name(self):
        return self.TAB_NAME or type(self).__name__.replace("_", " ").capitalize()

    def is_active(self):
        return "pf-m-current" in self.parent_browser.classes(self.TAB_LOCATOR)

    @property
    def is_displayed(self):
        return self.parent_browser.is_displayed(self.TAB_LOCATOR)

    def click(self):
        return self.parent_browser.click(self.TAB_LOCATOR)

    def select(self):
        if not self.is_active():
            self.logger.info("Opening the tab %s", self.tab_name)
            self.click()

    def child_widget_accessed(self, widget):
        # Select the tab
        self.select()

    def __repr__(self):
        return "<Tab {!r}>".format(self.tab_name)
