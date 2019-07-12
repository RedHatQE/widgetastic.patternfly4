from .button import Button
from widgetastic.widget import ParametrizedLocator, Text, View
from wait_for import wait_for
from cached_property import cached_property
from widgetastic.xpath import quote


class ReadOnlyChip(Exception):
    def __init__(self, chip):
        super().__init__()
        self.chip = chip


class Chip(View):
    ROOT = ParametrizedLocator("{@locator}")

    CHIP_LOCATOR = ".//li[contains(@class, 'pf-c-chip') and not(contains(@class, 'pf-m-overflow'))]"

    _text = Text(".//span[contains(@class, 'pf-c-chip__text')]")
    _badge = Text(
        ".//span[contains(@class, 'pf-c-chip__text')]/span[contains(@class, 'pf-c-badge')]"
    )
    button = Button(**{"aria-label": "close"})

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator or self.CHIP_LOCATOR

    @cached_property
    def text(self):
        """
        Return the text displayed on the chip

        A chip's text will never change, so we can cache this property
        Note that text is defined differently below in OverflowChip
        """
        if self.badge:
            # If this chip has a badge, strip the badge off the end to return only the text
            return self._text.text.rstrip(self.badge)
        return self._text.text

    @cached_property
    def badge(self):
        """
        Return the text of the badge displayed on the chip, if it has a badge

        A chip's badge will never change, so we can cache this property
        """
        return self._badge.text if self._badge.is_displayed else None

    @property
    def is_displayed(self):
        return self._text.is_displayed

    @cached_property
    def read_only(self):
        """
        Return whether or not this chip is read-only

        This will never change for a chip, so we can cache this property
        """
        return not self.button.is_displayed

    def read(self):
        return self.text

    def remove(self):
        def _gone():
            return not self.is_displayed

        if not self.read_only:
            self.button.click()
            wait_for(_gone, num_sec=3, message="wait for chip to dissappear", delay=0.1)
        else:
            raise ReadOnlyChip(self, "Chip is read-only")


class OverflowChip(Chip):
    """
    The 'Show More'/'Show Less' button is essentially a special kind of chip
    """

    CHIP_LOCATOR = (
        ".//*[(self::li or self::div) and "
        "contains(@class, 'pf-c-chip') and contains(@class, 'pf-m-overflow')]"
    )

    @property
    def is_displayed(self):
        return self.button.is_displayed

    @property
    def read_only(self):
        """
        Override to always return False here, since the button on this chip is always clickable
        """
        return False

    @property
    def text(self):
        """
        Override the text property so this is not a cached property, since button text can change
        """
        return self._text.text

    def _show_less_shown(self):
        return self.text.replace(" ", "").lower() == "showless"

    def _show_more_shown(self):
        return "more" in self.text.lower()

    def show_more(self):
        if self._show_more_shown():
            self._text.click()
        wait_for(
            func=self._show_less_shown,
            num_sec=3,
            delay=0.1,
            message="wait for 'show less' button to appear",
        )

    def show_less(self):
        if self._show_less_shown():
            self._text.click()
        wait_for(
            self._show_more_shown,
            num_sec=3,
            delay=0.1,
            message="wait for 'show more' button to appear",
        )


class ChipGroup(View):
    ROOT = ParametrizedLocator("{@locator}")

    CHIPS_LOCATOR = Chip.CHIP_LOCATOR
    GROUP_LOCATOR = ".//ul[contains(@class, 'pf-c-chip-group')]"
    LABEL_LOCATOR = "./preceding-sibling::*[contains(@class, 'pf-c-chip-group__label')]"

    overflow = OverflowChip()

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator or self.GROUP_LOCATOR

    @property
    def label(self):
        if isinstance(self.parent, ChipGroupToolbarCategory):
            return self.parent.label

        # It's unlikely we'll have a labelled chip group that is not in a toolbar
        # ... but just in case
        elements = self.browser.elements(self.LABEL_LOCATOR)
        return elements[0].text if elements else None

    def show_more(self):
        self.overflow.show_more()

    def show_less(self):
        self.overflow.show_less()

    @property
    def multiselect(self):
        return self.overflow.is_displayed

    def get_chips(self, show_more=True):
        if self.multiselect and show_more:
            self.show_more()
        chip_elements = self.browser.elements(self.CHIPS_LOCATOR)

        chips = []
        for el in chip_elements:
            # Track the chip by text instead of position, because its position in the row can
            # change
            chip_text = quote(self.browser.text(el))
            chips.append(Chip(parent=self, locator=f"{self.CHIPS_LOCATOR}[(.)={chip_text}]"))

        return chips

    def __iter__(self):
        for chip in self.get_chips():
            yield chip

    def remove_chip_by_name(self, name):
        for chip in self.get_chips():
            if chip.text.lower() == name.lower():
                chip.remove()
                break
        else:
            raise ValueError(f"Could not find chip with name '{name}'")

    def remove_all_chips(self):
        for chip in self.get_chips():
            chip.remove()

    def read(self):
        return [chip.text for chip in self]


class ChipGroupToolbarCategory(View):
    ROOT = ParametrizedLocator("{@locator}")
    GROUP_LOCATOR = "./ul[contains(@class, 'pf-c-chip-group') and contains(@class, 'pf-m-toolbar')]"
    LABEL_LOCATOR = "./li/*[contains(@class, 'pf-c-chip-group__label')]"

    _label = Text(LABEL_LOCATOR)

    def _gen_locator(self, label, locator):
        if locator:
            loc = locator
        else:
            if label:
                loc = f"{self.GROUP_LOCATOR}[{self.LABEL_LOCATOR}[(.)={label}]]"
            else:
                loc = self.GROUP_LOCATOR
        return loc

    def __init__(self, parent, label=None, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = self._gen_locator(label, locator)

    @property
    def label(self):
        return self._label.text


class ChipGroupToolbar(View):
    ROOT = ParametrizedLocator("{@locator}")

    # The parent of the chip group toolbar can be any element type
    # The locator should be the parent node which holds all the pf-c-chip-group elements
    TOOLBAR_LOCATOR = (
        ".//ul[contains(@class, 'pf-c-chip-group') and "
        "contains(@class, 'pf-m-toolbar')]/parent::*"
    )

    overflow = OverflowChip(
        locator=("./div[contains(@class, 'pf-c-chip') and contains(@class, 'pf-m-overflow')]")
    )

    def __init__(self, parent, locator=None, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator or self.TOOLBAR_LOCATOR

    def get_groups(self, show_more=True):
        if self.overflow.is_displayed and show_more:
            self.overflow.show_more()

        group_elements = self.browser.elements(ChipGroupToolbarCategory.GROUP_LOCATOR)
        group_list = []
        for idx, el in enumerate(group_elements):
            # The parent of this chip group needs to be the category group, not 'self' which is the
            # whole toolbar. We track the group by text instead of position, because its position
            # in the row can change.
            #
            # Get the text of the group's label first
            temp_toolbar_group = ChipGroupToolbarCategory(
                locator=f"{ChipGroupToolbarCategory.GROUP_LOCATOR}[{idx + 1}]", parent=self
            )
            group_text = quote(temp_toolbar_group.label)
            # Create a new toolbar widget, using a text locator
            toolbar_group = ChipGroupToolbarCategory(label=group_text, parent=self)
            # Finally create a chip group, whose parent is this toolbar group
            group_list.append(ChipGroup(parent=toolbar_group))
        return group_list

    def __iter__(self):
        for group in self.get_groups():
            yield group

    def read(self):
        groups = {}
        for group in self:
            groups[group.label] = group.read()
        return groups

    def show_more(self):
        self.overflow.show_more()

    def show_less(self):
        self.overflow.show_less()
