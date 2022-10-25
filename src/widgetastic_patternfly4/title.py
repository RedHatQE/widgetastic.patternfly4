from widgetastic.widget import ParametrizedLocator
from widgetastic.widget import Widget


class BaseTitle:
    """Base class for PF4 title widget

    Simple widget, but it has component classes and variable heading
    """

    @property
    def heading_level(self):
        return self.browser.element(self, parent=self.parent).tag_name

    @property
    def text(self):
        return self.browser.text(self, parent=self.parent)

    def read(self):
        return self.text


class Title(BaseTitle, Widget):
    ROOT = ParametrizedLocator(
        ".//*[(self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6) "
        "and (contains(@class, 'pf-c-title') "
        "and normalize-space(.)={@expected|quote})]"
    )

    def __init__(self, parent, text, **kwargs):
        """Using text for parametrized locator renders read/text methods largely useless"""
        super().__init__(parent, **kwargs)
        self.expected = text
