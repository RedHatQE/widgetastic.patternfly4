from .dropdown import Dropdown


class BaseOptionsMenu:
    BUTTON_LOCATOR = (
        ".//button[contains(@class, 'pf-c-options-menu__toggle') or "
        "contains(@class, 'pf-c-options-menu__toggle-button')]"
    )
    ITEMS_LOCATOR = ".//ul[contains(@class, 'pf-c-options-menu__menu')]/li"
    ITEM_LOCATOR = (
        ".//*[contains(@class, 'pf-c-options-menu__menu-item') and normalize-space(.)={}]"
    )
    TEXT_LOCATOR = (
        './/div[contains(@class, "pf-c-options-menu") and '
        'descendant::span[contains(@class, "pf-c-options-menu__toggle-text") and '
        "normalize-space(.)={}]]"
    )
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-options-menu")][1]'

    SELECTED_ITEMS_LOCATOR = (
        f"{ITEMS_LOCATOR}/button[.//*[name()='svg'] or descendant::i[not(@hidden)]]"
    )

    @property
    def selected_items(self):
        """Returns a list of all selected items in the options menu."""
        with self.opened():
            return [
                self.browser.text(el) for el in self.browser.elements(self.SELECTED_ITEMS_LOCATOR)
            ]


class OptionsMenu(BaseOptionsMenu, Dropdown):
    pass
