from selenium.webdriver.support.ui import Select
from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import GenericLocatorWidget


class FormSelectDisabled(Exception):
    """Raised if the FormSelect is Disabled."""

    pass


class FormSelectOptionDisabled(Exception):
    """Raise if the specific option chosen is disabled."""

    pass


class FormSelectOptionNotFound(Exception):
    """Raised if the specific form option is not found in the form select."""

    pass


class BaseFormSelect:
    """Represents the Patternfly FormSelect.

    https://www.patternfly.org/v4/documentation/react/components/formselect
    """

    ALL_OPTIONS_LOCATOR = ".//option"
    PARENT_OPTION_GROUP = "./parent::optgroup"

    @property
    def is_enabled(self):
        """Returns whether the FormSelect itself is enabled and therefore interactive."""
        return self.browser.get_attribute("disabled", self) is None

    @property
    def is_valid(self):
        """Returns whether the FormSelect has valid option selected - not highlighted with red
        color and special icon.
        """
        return self.browser.get_attribute("aria-invalid", self) == "false"

    @property
    def all_options(self):
        """Returns a list of all the options in the FormSelect."""
        return [self.browser.text(el) for el in self.browser.elements(self.ALL_OPTIONS_LOCATOR)]

    @property
    def all_enabled_options(self):
        """Returns a list of all enabled options in the FormSelect.

        Options might be disabled by `disabled` attr in their WebElement or in parent optgroup
        element (if it exists)."""
        result = []
        all_option_elements = self.browser.elements(self.ALL_OPTIONS_LOCATOR)
        for el in all_option_elements:
            try:
                group_disabled = (
                    self.browser.get_attribute("disabled", self.PARENT_OPTION_GROUP, parent=el)
                    is not None
                )
            except NoSuchElementException:
                group_disabled = False
            element_disabled = self.browser.get_attribute("disabled", el) is not None
            if not group_disabled and not element_disabled:
                result.append(self.browser.text(el))
        return result

    @property
    def _select_element(self):
        return Select(self.__element__())

    def fill(self, value):
        """Select desired option in FormSelect.

        Raises:
            FormSelectDisabled: if FormSelect is disabled
            FormSelectOptionDisabled: if option or entire optgroup is disabled
            FormSelectOptionNotFound: if option not found
        """
        if not self.is_enabled:
            raise FormSelectDisabled("{} is not enabled".format(repr(self)))
        if value not in self.all_options:
            raise FormSelectOptionNotFound(
                'Option "{}" not found in {}. Available options: {}'.format(
                    value, repr(self), self.all_options
                )
            )
        elif value not in self.all_enabled_options:
            raise FormSelectOptionDisabled(
                'Option "{}" is disabled in {}. Enabled options are: {}'.format(
                    value, repr(self), self.all_enabled_options
                )
            )
        self._select_element.select_by_visible_text(value)

    def read(self):
        """Returns selected option."""
        return self.browser.text(self._select_element.first_selected_option)

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.locator)


class FormSelect(BaseFormSelect, GenericLocatorWidget):
    pass
