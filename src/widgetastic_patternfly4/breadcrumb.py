from widgetastic.exceptions import WidgetOperationFailed
from widgetastic.widget import Widget


class BaseBreadCrumb:
    """Represents the Patternfly BreadCrumb.

    https://www.patternfly.org/v4/documentation/react/components/breadcrumb
    """

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

    def click_location(self, name, partial=False, handle_alert=False):
        """Clicks a location present in the breadcrumbs by string name.

        Args:
            name: location name
            partial(bool): Whether to use partial match
            handle_alert: handle the browser alert and ensure page safe
        """
        try:
            location = next(
                loc
                for loc in self._path_elements
                if (not partial and (self.browser.text(loc) == name))
                or (partial and (name in self.browser.text(loc)))
            )
        except StopIteration:
            partial_msg = " with partial match" if partial else ""
            locs = f" within locations: {self.locations}"
            raise WidgetOperationFailed(
                f'Breadcrumb location "{name}" not found{partial_msg}{locs}'
            )
        self.browser.click(location, ignore_ajax=handle_alert)
        if handle_alert:
            self.browser.handle_alert(wait=2.0)
            self.browser.plugin.ensure_page_safe()

    def read(self):
        """Return the active location of the breadcrumb."""
        return self.active_location


class BreadCrumb(BaseBreadCrumb, Widget):
    ROOT = './/nav[contains(@class, "pf-c-breadcrumb")]/ol'
