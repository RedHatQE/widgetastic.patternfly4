from widgetastic.log import call_sig
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import ClickableMixin, Widget
from widgetastic.xpath import quote


class Button(Widget, ClickableMixin):
    """A Patternfly button

    You can match by text, partial text or by attributes, you can also add the patternfly classes
    into the matching.

    .. code-block:: python

        Button("Text of button (unless it is an input ...)")
        Button("contains", "Text of button (unless it is an input ...)")
        Button(title="Show xyz")  # And such
        Button("Add", classes=[Button.PRIMARY])
        assert button.active
        assert not button.disabled
    """

    ROOT = ParametrizedLocator(
        ".//*[(self::a or self::button or (self::input and "
        '(@type="button" or @type="submit"))) and '
        'contains(@class, "pf-c-button") {@locator_conditions}]'
    )
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

    def __init__(self, parent, *text, **kwargs):
        logger = kwargs.pop("logger", None)
        Widget.__init__(self, parent, logger=logger)
        self.args = text
        self.kwargs = kwargs
        classes = kwargs.pop("classes", [])
        if text:
            if kwargs:  # classes should have been the only kwarg combined with text args
                raise TypeError("If you pass button text then only pass classes in addition")
            if len(text) == 1:
                self.locator_conditions = "normalize-space(.)={}".format(quote(text[0]))
            elif len(text) == 2 and text[0].lower() == "contains":
                self.locator_conditions = "contains(normalize-space(.), {})".format(quote(text[1]))
            else:
                raise TypeError("An illegal combination of text params")
        else:
            # Join the kwargs, if any
            self.locator_conditions = " and ".join(
                "@{}={}".format(attr, quote(value)) for attr, value in kwargs.items()
            )

        if classes:
            if self.locator_conditions:
                self.locator_conditions += " and "
            self.locator_conditions += " and ".join(
                "contains(@class, {})".format(quote(klass)) for klass in classes
            )
        if self.locator_conditions:
            self.locator_conditions = "and ({})".format(self.locator_conditions)

    @property
    def active(self):
        return "pf-m-active" in self.browser.classes(self)

    @property
    def disabled(self):
        return (
            "pf-m-disabled" in self.browser.classes(self) or
            self.browser.get_attribute("disabled", self) == "disabled"
        )

    def __repr__(self):
        return "{}{}".format(type(self).__name__, call_sig(self.args, self.kwargs))

    @property
    def title(self):
        return self.browser.get_attribute("title", self)
