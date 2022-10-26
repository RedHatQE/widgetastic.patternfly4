from widgetastic.widget import Checkbox
from widgetastic.widget import ParametrizedLocator
from widgetastic.widget import Text
from widgetastic.widget import View

# https://patternfly-react.surge.sh/components/radio


class BaseRadio:
    ROOT_ID_LOC = ParametrizedLocator(
        ".//div[contains(@class, 'pf-c-radio') and .//input[@type='radio' and @id={@id|quote}]]"
    )
    ROOT_LABEL_LOC = ParametrizedLocator(
        ".//div[contains(@class, 'pf-c-radio') and "
        ".//*[contains(@class, 'pf-c-radio__label') and normalize-space(.)={@label_text|quote}]]"
    )
    DESC_LOC = ".//*[contains(@class, 'pf-c-radio__description')]"
    BODY_LOC = ".//*[contains(@class, 'pf-c-radio__body')]"
    RADIO_LOC = ".//input[contains(@class, 'pf-c-radio__input')]"
    LABEL_LOC = ".//*[contains(@class, 'pf-c-radio__label')]"

    def __init__(self, parent, id=None, label_text=None, **kwargs):
        """Generate locator based on either id or label (but not both)"""
        super().__init__(parent, **kwargs)
        if id is not None and label_text is not None:
            raise TypeError("Cannot create Radio with id and label set")
        self.id = id
        self.label_text = label_text
        self.locator = self.ROOT_ID_LOC if id is not None else self.ROOT_LABEL_LOC

    @property
    def body(self):
        """Consider nesting a view when subclassing to override and add widgets"""
        return self.browser.element(self.BODY_LOC)


class Radio(BaseRadio, View):
    """Base Radio view, subclass to add widgets to the body"""

    ROOT = ParametrizedLocator("{@locator}")

    description = Text(BaseRadio.DESC_LOC)
    radio = Checkbox(locator=BaseRadio.RADIO_LOC)
    label = Text(BaseRadio.LABEL_LOC)
    body = Text(BaseRadio.BODY_LOC)  # subclass + View.nested class to inject body with more widgets

    @property
    def selected(self):
        return self.radio.selected

    @property
    def disabled(self):
        return "pf-m-disabled" in self.browser.classes(self.label)

    def fill(self, values):
        """Can only handle `True` to check the radio, nature of individual radio button"""
        return self.radio.fill(values)


# TODO there is a 'name' attribute used by PF for correlating radio buttons
# This could be used to create a `RadioGroup` class of Radio widgets
