# widgetastic.patternfly4

[![Build status](https://github.com/RedHatQE/widgetastic.patternfly4/workflows/wt.pf4%20tests/badge.svg)](https://github.com/RedHatQE/widgetastic.patternfly4/actions)
[![codecov](https://codecov.io/gh/RedHatQE/widgetastic.patternfly4/branch/master/graph/badge.svg)](https://codecov.io/gh/RedHatQE/widgetastic.patternfly4)
[![PyPI version](https://badge.fury.io/py/widgetastic.patternfly4.svg)](https://badge.fury.io/py/widgetastic.patternfly4)
[![Documentation status](https://readthedocs.org/projects/widgetasticpatternfly4/badge/?version=latest)](https://widgetasticpatternfly4.readthedocs.io/en/latest/?badge=latest)

Library of Patternfly v4 (aka Next) components for [Widgetastic](https://github.com/RedHatQE/widgetastic.core).

## Components list

Alert - <https://www.patternfly.org/v4/components/alert>

Breadcrumb - <https://www.patternfly.org/v4/components/breadcrumb>

Button - <https://www.patternfly.org/v4/components/button>

Bullet Chart - <https://www.patternfly.org/v4/charts/bullet-chart>

Card - <https://www.patternfly.org/v4/components/card>

Chip Group - <https://www.patternfly.org/v4/components/chip-group>

Context Selector - <https://www.patternfly.org/v4/components/context-selector>

Donut Chart - <https://www.patternfly.org/v4/charts/donut-chart>

Dropdown - <https://www.patternfly.org/v4/components/dropdown>

FormSelect - <https://www.patternfly.org/v4/components/form-select>

Menu - <https://www.patternfly.org/v4/components/menu>

Modal - <https://www.patternfly.org/v4/components/modal>

Nav - <https://www.patternfly.org/v4/components/navigation>

Options Menu - <https://www.patternfly.org/v4/components/options-menu>

Pagination - <https://www.patternfly.org/v4/components/pagination>

Pie Chart - <https://www.patternfly.org/v4/charts/pie-chart>

Popover - <https://www.patternfly.org/v4/components/popover>

Progress - <https://www.patternfly.org/v4/components/progress>

Select - <https://www.patternfly.org/v4/components/select>

Switch - <https://www.patternfly.org/v4/components/switch>

Table - <https://www.patternfly.org/v4/components/table>

Tabs - <https://www.patternfly.org/v4/components/tabs>

## Contribution guide

```bash
# create a virtual environment
python3 -m venv /path/to/your/virtualenv/wt.pf4
source /path/to/your/virtualenv/wt.pf4/bin/activate

# update pip and its friends
pip install -U pip setuptools wheel

# clone the repo
git clone https://github.com/RedHatQE/widgetastic.patternfly4.git

# install pre-commit
cd widgetastic.patternfly4
# install the package in editable mode
pip install -e .[dev]
pre-commit install
```

## Testing

The library has selenium tests that are performed against [Patternfly React docs](https://patternfly-react.surge.sh/patternfly-4/).
It's also configured to run the tests every time when a new version of that page is released.
Tests spawn a container from `quay.io/redhatqe/selenium-standalone` image. It has configured
Selenium standalone server and the browsers (Chrome and Firefox).

**Note:** Tests use `podman` to manage containers. Please install it before running.

It's possible to run tests in parallel to speed up the execution. Use `-n` key tp specify a number
of workers:

```bash
BROWSER=firefox pytest -v testing -n 4
```
