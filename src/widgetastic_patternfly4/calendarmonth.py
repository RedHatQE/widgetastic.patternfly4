from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import Widget
from widgetastic.xpath import quote

from .select import Select


class DisabledDate(Exception):
    pass


class BaseCalendarMonth:
    """Represents calendar month component.

    https://www.patternfly.org/v4/components/calendar-month
    """

    CALENDAR_HEADER = ".//div[@class='pf-c-calendar-month__header']"
    MONTH_SELECT_LOCATOR = (
        f"{CALENDAR_HEADER}//div[contains(@class, 'header-month')]"
        f"//div[@data-ouia-component-type='PF4/Select']"
    )
    _month_select_widget = Select(locator=MONTH_SELECT_LOCATOR)
    YEAR_INPUT_LOCATOR = f"{CALENDAR_HEADER}//div[contains(@class, 'header-year')]/input"
    DATE_LOCATOR = ".//button[text()={date}]"

    PREV_BUTTON_LOCATOR = f"{CALENDAR_HEADER}//div[contains(@class, 'prev-month')]"
    NEXT_BUTTON_LOCATOR = f"{CALENDAR_HEADER}//div[contains(@class, 'next-month')]"

    TABLE = ".//table"
    SELECTED_DATE_LOCATOR = f"{TABLE}/tbody//td[contains(@class, 'pf-m-selected')]"

    def prev(self):
        return self.browser.click(self.PREV_BUTTON_LOCATOR)

    def next(self):
        return self.browser.click(self.NEXT_BUTTON_LOCATOR)

    @property
    def year(self):
        el = self.browser.element(self.YEAR_INPUT_LOCATOR)
        return el.get_attribute("value")

    @year.setter
    def year(self, value):
        el = self.browser.element(self.YEAR_INPUT_LOCATOR)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(str(value) + Keys.ENTER)

    @property
    def month(self):
        el = self.browser.element(self.MONTH_SELECT_LOCATOR)
        return self.browser.text(el)

    @month.setter
    def month(self, value):
        self._month_select_widget.item_select(value)

    @property
    def day(self):
        try:
            el = self.browser.element(self.SELECTED_DATE_LOCATOR)
        except NoSuchElementException:
            return ""
        return self.browser.text(el)

    @day.setter
    def day(self, value):
        el = self.browser.element(self.DATE_LOCATOR.format(date=quote(value)))
        if "pf-m-disabled" in el.get_attribute("class") or el.get_attribute("disabled"):
            raise DisabledDate(f"Date {value} is disabled for selection")
        el.click()

    def read(self):
        """Returns the currently selected date in format DD MONTH YYYY."""
        return f"{self.day} {self.month} {self.year}"

    def fill(self, items):
        """Fills a Calendar with all items.
        Example dictionary: {'day': '22', 'month': 'November', 'year': '2023'}"

        Args:
            items: A dictionary containing what items to select
        """
        if type(items) is not dict:
            raise TypeError("'items' value has to be dictionary type. ")
        if "day" in items:
            self.day = items["day"]
        if "month" in items:
            self.month = items["month"]
        if "year" in items:
            self.year = items["year"]


class CalendarMonth(BaseCalendarMonth, Widget):
    ROOT = ParametrizedLocator("{@locator}")

    def __init__(self, parent, locator, logger=None):
        super().__init__(parent, logger=logger)
        self.locator = locator
