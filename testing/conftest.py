import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from widgetastic.browser import Browser


@pytest.fixture(scope="session")
def browser_name():
    return os.environ["BROWSER"]


@pytest.fixture(scope="module")
def selenium(browser_name):
    if browser_name == "firefox":
        driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX)
    elif browser_name == "chrome":
        caps = DesiredCapabilities.CHROME.copy()
        caps["chromeOptions"] = {"args": ["disable-dev-shm-usage", "no-sandbox"]}
        driver = webdriver.Remote(desired_capabilities=caps)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser(selenium, request):
    name = request.module.__name__.split("_")[1]
    category = getattr(request.module, "CATEGORY", "components")
    url = "https://patternfly-react.surge.sh/patternfly-4/documentation/react/{}/{}"
    selenium.maximize_window()
    selenium.get(url.format(category, name))
    return Browser(selenium)
