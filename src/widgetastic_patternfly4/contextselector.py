from . import Select


class ContextSelector(Select):
    ITEMS_LOCATOR = ".//ul[@class='pf-c-context-selector__menu-list']/li"
    ITEM_LOCATOR = (".//button[contains(@class, 'pf-c-context-selector__menu-list-item')"
                    " and normalize-space(.)={}]")
    SEARCH_INPUT_LOCATOR = ".//input[@type='search']"
    SEARCH_BUTTON_LOCATOR = ".//button[contains(@id, 'pf-context-selector-search-button')]"

    def item_select(self, item, use_search=False):
        """Opens the Context Selector and selects the desired item.

        Args:
            item: Item to be selected
            use_search: whether to search for item before selecting it
        """
        self.logger.info("Selecting %r in %r", item, self)
        with self.opened():
            if use_search:
                self.browser.send_keys(item, self.SEARCH_INPUT_LOCATOR)
                self.browser.click(self.SEARCH_BUTTON_LOCATOR)
            self.browser.click(self.item_element(item, close=False))
