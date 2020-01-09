from widgetastic.widget import Widget


class BreadCrumb(Widget):
    """Represents the Patternfly BreadCrumb.

    https://www.patternfly.org/v4/documentation/react/components/breadcrumb
    """

    ROOT = './/nav[contains(@class, "pf-c-breadcrumb")]/ol'
    ELEMENTS = ".//li"

    @property
    def _path_elements(self):
        return self.browser.elements(self.ELEMENTS)

    @property
    def locations(self):
        """Returns a list of strings of the current location according to the breadcrumbs."""
        return [self.browser.text(loc) for loc in self._path_elements]

    @property
    def active_location(self):
        """Returns the last location in the breadcrumb, or None if breadcrumbs are not present/set.
        """
        return self.locations[-1] if self.locations else None

    def click_location(self, name, handle_alert=False):
        """Clicks a location present in the breadcrumbs by string name.
        """
        location = next(loc for loc in self._path_elements if self.browser.text(loc) == name)
        self.browser.click(location, ignore_ajax=handle_alert)
        if handle_alert:
            self.browser.handle_alert(wait=2.0)
            self.browser.plugin.ensure_page_safe()

    def read(self):
        """Return the active location of the breadcrumb."""
        return self.active_location
