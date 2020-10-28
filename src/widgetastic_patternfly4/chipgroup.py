from wait_for import wait_for
from widgetastic.widget import ParametrizedLocator
from widgetastic.widget import ParametrizedView
from widgetastic.widget import Text
from widgetastic.widget import View

from .button import Button


class ChipReadOnlyError(Exception):
    def __init__(self, chip, message):
        super().__init__(message)
        self.chip = chip


CHIP_ROOT = ".//div[@class='pf-c-chip' and not(contains(@class, 'pf-m-overflow'))]"
CHIP_TEXT = ".//span[contains(@class, 'pf-c-chip__text')]"
CHIP_BADGE = ".//span[contains(@class, 'pf-c-badge')]"
GROUP_ROOT = ".//div[contains(@class, 'pf-c-chip-group')]"
CATEGORY_GROUP_ROOT = (
    ".//div[contains(@class, 'pf-c-chip-group') and contains(@class, 'pf-m-category')]"
)
CATEGORY_LABEL = ".//span[contains(@class, 'pf-c-chip-group__label')]"
CATEGORY_CLOSE = "./div[contains(@class, 'pf-c-chip-group__close')]/button"
# For backwards compatibility
OLD_GROUP_ROOT = ".//ul[contains(@class, 'pf-c-chip-group')]"
TOOLBAR_GROUP_LABEL = "./li/*[contains(@class, 'pf-c-chip-group__label')]"
STANDALONE_GROUP_LABEL = "./preceding-sibling::*[contains(@class, 'pf-c-chip-group__label')]"
OLD_CHIP_ROOT = (
    ".//*[(self::div or self::li) and contains(@class, 'pf-c-chip') "
    "and not(contains(@class, 'pf-m-overflow'))]"
)


class _BaseChip(View):
    """
    Holds attributes shared by both Chip and OverflowChip
    """

    _text = Text(CHIP_TEXT)
    _badge = Text(f"{CHIP_TEXT}/{CHIP_BADGE}")
    button = Button(**{"aria-label": "close"})

    @property
    def badge(self):
        """
        Return the text of the badge displayed on the chip, if it has a badge
        """
        return self._badge.text if self._badge.is_displayed else None

    @property
    def text(self):
        """
        Return the text displayed on the chip
        """
        if self.badge:
            # If this chip has a badge, strip the badge off the end to return only the text
            return self._text.text.rstrip(self.badge)
        return self._text.text

    @property
    def is_displayed(self):
        """Returns True if the component is displayed."""
        return self._text.is_displayed

    def read(self):
        """Returns the text of the Chip as a string"""
        return self.text


class Chip(ParametrizedView, _BaseChip):
    PARAMETERS = ("text",)
    ROOT = ParametrizedLocator(
        f"{CHIP_ROOT}[{CHIP_TEXT}[starts-with(normalize-space(.), {{text|quote}})]]"
    )

    @staticmethod
    def _get_text_ignoring_badge(browser, element):
        el = element
        badge_elements = browser.elements(CHIP_BADGE, parent=el)
        if badge_elements:
            badge = browser.text(el)
            return badge.rstrip(browser.text(badge_elements[0]))
        return browser.text(el)

    @classmethod
    def all(cls, browser):
        """Returns a list of the text of each chip"""
        return [
            (cls._get_text_ignoring_badge(browser, el),)
            for el in browser.elements(f"{CHIP_ROOT}/{CHIP_TEXT}")
        ]

    def __init__(self, *args, **kwargs):
        ParametrizedView.__init__(self, *args, **kwargs)

    def remove(self):
        """Removes a chip"""

        def _gone():
            return not self.is_displayed

        if not self.read_only:
            self.button.click()
            wait_for(_gone, num_sec=3, message="wait for chip to dissappear", delay=0.1)
        else:
            raise ChipReadOnlyError(self, "Chip is read-only")

    @property
    def read_only(self):
        """Returns a boolean detailing if the chip is read only"""
        return not self.button.is_displayed


class OverflowChip(_BaseChip):
    """
    The 'Show More'/'Show Less' button is essentially a special kind of chip
    """

    ROOT = ".//button[contains(@class, 'pf-c-chip') and contains(@class, 'pf-m-overflow')]"

    def _show_less_shown(self):
        return self.text.replace(" ", "").lower() == "showless"

    def _show_more_shown(self):
        return "more" in self.text.lower()

    def show_more(self):
        """Expands a chip group"""
        if self._show_more_shown():
            self._text.click()
        wait_for(
            func=self._show_less_shown,
            num_sec=3,
            delay=0.1,
            message="wait for 'show less' button to appear",
        )

    def show_less(self):
        """Collapses a chip group"""
        if self._show_less_shown():
            self._text.click()
        wait_for(
            self._show_more_shown,
            num_sec=3,
            delay=0.1,
            message="wait for 'show more' button to appear",
        )


class ChipGroup(View):
    """
    Represents a chip group that is "on its own", i.e. not a part of a chip group category
    """

    ROOT = ParametrizedLocator("{@locator}")

    overflow = OverflowChip()
    chips = ParametrizedView.nested(Chip)

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator or GROUP_ROOT

    # For backwards compatibility
    @property
    def label(self):
        # It's unlikely we'll have a labelled chip group that is not in a toolbar
        # ... but just in case
        elements = self.browser.elements(STANDALONE_GROUP_LABEL)
        return self.browser.text(elements[0]) if elements else None

    # For backwards compatibility
    @property
    def is_multiselect(self):
        return self.overflow.is_displayed

    def show_more(self):
        """Expands a chip group"""
        self.overflow.show_more()

    def show_less(self):
        """Collapses a chip group"""
        self.overflow.show_less()

    def get_chips(self, show_more=True):
        """
        A helper to expand the chip group before reading its chips
        """
        if self.overflow.is_displayed and show_more:
            self.show_more()
        return self.chips

    @property
    def has_chips(self):
        return self.is_displayed

    def __iter__(self):
        chips = self.get_chips()
        for chip in chips:
            yield chip

    def remove_chip_by_name(self, name):
        """Removes a chip from the group by name"""
        for chip in self:
            if chip.text.lower() == name.lower():
                chip.remove()
                break
        else:
            raise ValueError(f"Could not find chip with name '{name}'")

    def remove_all_chips(self):
        """Removes all chips from the group"""
        for chip in self:
            chip.remove()

    def read(self):
        self.logger.info(self.get_chips())
        return [chip.text for chip in self]


class CategoryChipGroup(ChipGroup):
    """
    Represents a Chip Group with a category label
    """

    ROOT = ParametrizedLocator(
        f"{CATEGORY_GROUP_ROOT}[{CATEGORY_LABEL}[normalize-space(.)={{@_label|quote}}]]"
    )

    chips = ParametrizedView.nested(Chip)
    close_button = Button(locator=CATEGORY_CLOSE)

    def __init__(self, parent, label, logger=None):
        self._label = label
        ChipGroup.__init__(self, parent, logger=logger)

    @property
    def label(self):
        elements = self.browser.elements(CATEGORY_LABEL)
        return self.browser.text(elements[0]) if elements else None

    @property
    def can_close(self):
        return self.close_button.is_displayed

    def close(self):
        self.close_button.click()

    @classmethod
    def all(cls, browser):
        """Returns a list of all category labels."""
        return [browser.text(el) for el in browser.elements(CATEGORY_LABEL)]


# For backwards compatibility
class OldChip(Chip):
    ROOT = ParametrizedLocator(
        f"{OLD_CHIP_ROOT}[{CHIP_TEXT}[starts-with(normalize-space(.), {{text|quote}})]]"
    )

    @classmethod
    def all(cls, browser):
        """Returns a list of the text of each chip"""
        return [
            (cls._get_text_ignoring_badge(browser, el),)
            for el in browser.elements(f"{OLD_CHIP_ROOT}/{CHIP_TEXT}")
        ]


# For backwards compatibility
class OldOverflowChip(OverflowChip):
    ROOT = (
        ".//*[(self::li or self::div) and "
        "contains(@class, 'pf-c-chip') and contains(@class, 'pf-m-overflow')]"
    )

    @property
    def is_displayed(self):
        """Returns a boolean detailing if the overflow chip is displayed"""
        return self.button.is_displayed


# For backwards compatibility
class StandAloneChipGroup(ChipGroup):
    chips = ParametrizedView.nested(OldChip)
    overflow = ParametrizedView.nested(OldOverflowChip)


# For backwards compatibility
class ChipGroupToolbarCategory(ParametrizedView, ChipGroup):
    """
    Represents a chip group that is part of a toolbar, identifiable by a category label
    """

    PARAMETERS = ("label",)
    ROOT = ParametrizedLocator(
        f"{OLD_GROUP_ROOT}[{TOOLBAR_GROUP_LABEL}[normalize-space(.)={{label|quote}}]]"
    )

    chips = ParametrizedView.nested(OldChip)

    def __init__(self, *args, **kwargs):
        ParametrizedView.__init__(self, *args, **kwargs)

    @property
    def label(self):
        elements = self.browser.elements(CATEGORY_LABEL)
        return self.browser.text(elements[0]) if elements else None

    @classmethod
    def all(cls, browser):
        return [
            (browser.text(el),)
            for el in browser.elements(f"{OLD_GROUP_ROOT}/{TOOLBAR_GROUP_LABEL}")
        ]


# For backwards compatibility
class ChipGroupToolbar(View):
    ROOT = ParametrizedLocator("{@locator}")

    # The parent of the chip group toolbar can be any element type
    # The locator should be the parent node which holds all the pf-c-chip-group elements
    TOOLBAR_LOCATOR = (
        ".//ul[contains(@class, 'pf-c-chip-group') and "
        "contains(@class, 'pf-m-toolbar')]/parent::*"
    )

    overflow = OldOverflowChip(
        locator=("./div[contains(@class, 'pf-c-chip') and contains(@class, 'pf-m-overflow')]")
    )
    groups = ParametrizedView.nested(ChipGroupToolbarCategory)

    def __init__(self, parent, locator=None, logger=None):
        self.locator = locator or self.TOOLBAR_LOCATOR
        super().__init__(parent, logger=logger)

    def get_groups(self, show_more=True):
        """
        A helper to expand the chip group toolbar before reading its groups
        """
        if self.overflow.is_displayed and show_more:
            self.overflow.show_more()
        return self.groups

    def __iter__(self):
        for group in self.get_groups():
            yield group

    def read(self):
        """Returns a dict of chips"""
        groups = {}
        for group in self:
            groups[group.label] = group.read()
        return groups

    def show_more(self):
        """Expands a chip group"""
        self.overflow.show_more()

    def show_less(self):
        """Collapses a chip group"""
        self.overflow.show_less()

    @property
    def has_chips(self):
        # If we delete all chips the ROOT is still shown thus we need to check if there are
        # any chips.
        return self.read() != {}
