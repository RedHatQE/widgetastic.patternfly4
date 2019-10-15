from .dropdown import Dropdown


class OptionsMenu(Dropdown):
    BUTTON_LOCATOR = (
        ".//button[contains(@class, 'pf-c-options-menu__toggle') or "
        "contains(@class, 'pf-c-options-menu__toggle-button')]"
    )
    ITEMS_LOCATOR = ".//ul[contains(@class, 'pf-c-options-menu__menu')]/li"
    ITEM_LOCATOR = (
        ".//button[contains(@class, 'pf-c-options-menu__menu-item')"
        " and normalize-space(.)={}]"
    )
    TEXT_LOCATOR = (
        './/div[contains(@class, "pf-c-options-menu") and '
        'descendant::span[contains(@class, "pf-c-options-menu__toggle-text") and '
        'normalize-space(.)={}]]'
    )
    DEFAULT_LOCATOR = './/div[contains(@class, "pf-c-options-menu")][1]'
