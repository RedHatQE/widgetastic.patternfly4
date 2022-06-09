from selenium.webdriver.common.keys import Keys
from widgetastic.widget import GenericLocatorWidget


class BaseSlider:
    """Represents the Patternfly-4 Slider.

    https://www.patternfly.org/v4/components/slider
    """

    LABELS = ".//div[contains(@class, 'pf-c-slider__step-label')]"
    THUMB = ".//div[contains(@class, 'pf-c-slider__thumb')]"
    STEPS = (
        ".//div[contains(@class, 'pf-c-slider__steps')]/"
        "child::div[contains(@class, 'pf-c-slider__step')]"
    )

    def _str_num(self, value):
        """Covert to integer if convertable.
        is_numeric not valid as we consider negative numbers as well.
        """
        try:
            return int(value)
        except ValueError:
            return value

    @property
    def is_enabled(self):
        """Check Slider is enabled or disabled."""
        return self.browser.get_attribute("aria-disabled", self.THUMB) == "false"

    @property
    def labels(self):
        """Returns a list of slider labels."""
        return [self._str_num(self.browser.text(el)) for el in self.browser.elements(self.LABELS)]

    @property
    def text(self):
        """Point current value of slider."""
        return self._str_num(self.browser.get_attribute("aria-valuenow", self.THUMB))

    @property
    def min(self):
        """Minimum value of slider."""
        return self._str_num(self.browser.get_attribute("aria-valuemin", self.THUMB))

    @property
    def max(self):
        """Maximum value of slider."""
        return self._str_num(self.browser.get_attribute("aria-valuemax", self.THUMB))

    @property
    def step(self):
        """Step size of slider."""
        return int((self.max - self.min) / (len(self.browser.elements(self.STEPS)) - 1))

    @property
    def _element_map(self):
        elements = {}
        step = self.step
        for index, el in enumerate(self.browser.elements(self.STEPS)):
            if index == 0:
                value = self.min
            else:
                value += step
            elements[value] = el
        return elements

    def steps(self):
        """Return all available steps."""
        return list(self._element_map.keys())

    def fill(self, value):
        """Fills a Slider with the supplied value."""
        if self.text == value:
            return False
        el_map = self._element_map
        target_el = el_map[value]
        source_el = el_map[self.text] if self.text in el_map else self.browser.element(self.THUMB)
        self.browser.move_to_element(source_el)
        self.browser.drag_and_drop(source_el, target_el)
        return True

    def read(self):
        """Read current slider value."""
        return self.text


class Slider(BaseSlider, GenericLocatorWidget):
    pass


class InputSlider(Slider):
    INPUT = ".//input"

    def fill(self, value):
        """Fills a Slider with the supplied value."""
        if self.text == value:
            return False
        el = self.browser.element(self.INPUT)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(str(value) + Keys.ENTER)
        return True
