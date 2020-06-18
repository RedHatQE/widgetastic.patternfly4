import re

from widgetastic_patternfly4 import BulletChart


class PieChart(BulletChart):
    """
    Represents the Pie Chart
    from Patternfly 4 (https://www.patternfly.org/v4/documentation/react/charts/chartpie)
    """

    APPLY_OFFSET = False
    LEGEND_ITEM_REGEX = re.compile(r"(\d+): (\w.*)|(\w.*): (\d+)")
