# widgetastic.patternfly4

[![Build Status](https://travis-ci.org/RedHatQE/widgetastic.patternfly4.svg?branch=master)](https://travis-ci.org/RedHatQE/widgetastic.patternfly4)
[![codecov](https://codecov.io/gh/RedHatQE/widgetastic.patternfly4/branch/master/graph/badge.svg)](https://codecov.io/gh/RedHatQE/widgetastic.patternfly4)
[![PyPI version](https://badge.fury.io/py/widgetastic.patternfly4.svg)](https://badge.fury.io/py/widgetastic.patternfly4)
[![Documentation Status](https://readthedocs.org/projects/widgetasticpatternfly4/badge/?version=latest)](https://widgetasticpatternfly4.readthedocs.io/en/latest/?badge=latest)

Library of Patternfly v4 (aka Next) components for [Widgetastic](https://github.com/RedHatQE/widgetastic.core).


### Components list

Alert - https://www.patternfly.org/v4/documentation/react/components/alert

Breadcrumb - https://www.patternfly.org/v4/documentation/react/components/breadcrumb

Button - https://www.patternfly.org/v4/documentation/react/components/button

Bullet Chart - https://www.patternfly.org/v4/documentation/react/charts/chartbullet

Chip Group - https://www.patternfly.org/v4/documentation/react/components/chipgroup

Context Selector - https://www.patternfly.org/v4/documentation/react/components/contextselector

Donut Chart - https://www.patternfly.org/v4/documentation/react/charts/chartdonut

Dropdown - https://www.patternfly.org/v4/documentation/react/components/dropdown

FormSelect - https://www.patternfly.org/v4/documentation/react/components/formselect

Modal - https://patternfly-react.surge.sh/v4/documentation/react/components/modal

Nav - https://www.patternfly.org/v4/documentation/react/components/nav

Options Menu - https://www.patternfly.org/v4/documentation/react/components/optionsmenu

Pagination - https://www.patternfly.org/v4/documentation/react/components/pagination

Pie Chart - https://www.patternfly.org/v4/documentation/react/charts/chartpie

Select - https://www.patternfly.org/v4/documentation/react/components/select

Switch - https://www.patternfly.org/v4/documentation/react/components/switch

Table - https://www.patternfly.org/v4/documentation/react/components/table

Tabs - https://www.patternfly.org/v4/documentation/react/components/tabs


### Contribution guide

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

### Testing

The library has selenium tests that are performed against [Patternfly React docs](https://patternfly-react.surge.sh/patternfly-4/).
It's also configured to run the tests every time when a new version of that page is released

```bash
# in order to run the tests you need to have selenium and browsers installed
# tests use docker container with all dependencies installed
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm quay.io/redhatqe/selenium-standalone
BROWSER=firefox pytest -v testing
```
