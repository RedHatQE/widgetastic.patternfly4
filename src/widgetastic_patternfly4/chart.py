from widgetastic.widget import Widget, ParametrizedLocator, ClickableMixin
from widgetastic.widget import Text
from widgetastic.xpath import quote

class DonutChart(Widget, ClickableMixin):
    """
        Represents the Donut Chart
        from Patternfly 4 (https://patternfly-react.surge.sh/patternfly-4/components/donutchart)
    """
    ROOT = ParametrizedLocator("{@locator}")
    BASE_LOCATOR = ".//div[@id={}]"
    PATH = ".//*[name()='svg']/*[name()='g']/*[name()='path']"
    total = Text(".//*[name()='svg']/*[name()='text']/*[name()='tspan']")
    tooltip = Text(".//div/*[name()='svg']/*[name()='g']/*[name()='text']/*[name()='tspan']")

    def __init__(self, parent, id=None, locator=None, logger=None):
        """Create the widget"""
        Widget.__init__(self, parent, logger=logger)
        if id:
            self.locator = self.BASE_LOCATOR.format(quote(id))
        elif locator:
            self.locator = locator
        else:
            raise TypeError("You need to specify either id or locator")
    def read(self):
        """read all the data in the chart"""
        data = []
        for el in self.browser.elements(self.PATH):
            self.browser.move_to_element(el)
            data.append(self.tooltip.read())
        return data
