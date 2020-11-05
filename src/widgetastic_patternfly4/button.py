from widgetastic.log import call_sig
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import ClickableMixin
from widgetastic.widget import Widget
from widgetastic.xpath import quote


class BaseButton:
    CHECK_VISIBILITY = True

    # Classes usable in the constructor
    # Button types
    PRIMARY = "pf-m-primary"
    SECONDARY = "pf-m-secondary"
    TETRIARY = "pf-m-tertiary"
    DANGER = "pf-m-danger"
    LINK = "pf-m-link"
    PLAIN = "pf-m-plain"

    # Shape
    BLOCK = "pf-m-block"

    def read(self):
        """Returns the string of the button."""
        return self.browser.text(self)

    @property
    def active(self):
        """Returns a boolean detailing if the button is active."""
        return "pf-m-active" in self.browser.classes(self)

    @property
    def disabled(self):
        """Returns a boolean detailing if the button is disabled."""
        check1 = "pf-m-disabled" in self.browser.classes(self)
        return check1 or self.browser.get_attribute("disabled", self)

    def __repr__(self):
        return "{}{}".format(type(self).__name__, call_sig(self.args, self.kwargs))

    @property
    def title(self):
        """Returns the title of the button as a string."""
        return self.browser.get_attribute("title", self)


class Button(BaseButton, Widget, ClickableMixin):
    """A Patternfly button

    You can match by text, partial text or by attributes, you can also add the patternfly classes
    into the matching.

    .. code-block:: python

        Button("Text of button (unless it is an input ...)")
        Button("contains", "Text of button (unless it is an input ...)")
        Button(title="Show xyz")  # And such
        Button("Add", classes=[Button.PRIMARY])
        Button(locator=".//xpath")
        assert button.active
        assert not button.disabled
    """

    ROOT = ParametrizedLocator("{@locator}")

    def _generate_locator(self, *text, **kwargs):
        classes = kwargs.pop("classes", [])
        if text:
            if kwargs:  # classes should have been the only kwarg combined with text args
                raise TypeError("If you pass button text then only pass classes in addition")
            if len(text) == 1:
                locator_conditions = "normalize-space(.)={}".format(quote(text[0]))
            elif len(text) == 2 and text[0].lower() == "contains":
                locator_conditions = "contains(normalize-space(.), {})".format(quote(text[1]))
            else:
                raise TypeError("An illegal combination of args/kwargs")
        else:
            # Join the kwargs, if any
            locator_conditions = " and ".join(
                "@{}={}".format(attr, quote(value)) for attr, value in kwargs.items()
            )

        if classes:
            if locator_conditions:
                locator_conditions += " and "
            locator_conditions += " and ".join(
                "contains(@class, {})".format(quote(klass)) for klass in classes
            )
        if locator_conditions:
            locator_conditions = "and ({})".format(locator_conditions)

        return (
            ".//*[(self::a or self::button or (self::input and "
            "(@type='button' or @type='submit'))) and "
            f"contains(@class, 'pf-c-button') {locator_conditions}]"
        )

    def __init__(self, parent, *text, **kwargs):
        super().__init__(parent, logger=kwargs.pop("logger", None))
        self.args = text
        self.kwargs = kwargs
        self.locator = kwargs.pop("locator", self._generate_locator(*text, **kwargs))
