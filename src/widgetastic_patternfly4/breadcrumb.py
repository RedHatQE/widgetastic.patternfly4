from widgetastic.widget import Widget


class BreadCrumb(Widget):
    """Represents the Patternfly BreadCrumb.

    http://patternfly-react.surge.sh/patternfly-4/components/breadcrumb
    """

    ROOT = './/nav[contains(@class, "pf-c-breadcrumb")]/ol'
    ELEMENTS = ".//li"

    def __init__(self, parent, locator=None, logger=None):
        Widget.__init__(self, parent=parent, logger=logger)
        self._locator = locator or self.ROOT

    def __locator__(self):
        return self._locator

    @property
    def _path_elements(self):
        return self.browser.elements(self.ELEMENTS)

    @property
    def locations(self):
        return [self.browser.text(loc) for loc in self._path_elements]

    @property
    def active_location(self):
        return self.locations[-1] if self.locations else None

    def click_location(self, name, handle_alert=False):
        location = next(loc for loc in self._path_elements if self.browser.text(loc) == name)
        self.browser.click(location, ignore_ajax=handle_alert)
        if handle_alert:
            self.browser.handle_alert(wait=2.0)
            self.browser.plugin.ensure_page_safe()

    def read(self):
        """Return the active location of the breadcrumb"""
        return self.active_location
