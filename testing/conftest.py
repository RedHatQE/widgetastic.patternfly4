import os

import pytest
from selenium import webdriver
from widgetastic.browser import Browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(scope="session")
def browser_name():
    return os.environ["BROWSER"]


@pytest.fixture(scope="session")
def selenium(browser_name):
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = True
        driver = webdriver.Firefox(options=firefox_options)
    elif browser_name == "remote":
        driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.CHROME)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser(selenium, request):
    name = request.module.__name__.split("_")[1]
    selenium.maximize_window()
    selenium.get("http://patternfly-react.surge.sh/patternfly-4/components/{}".format(name))
    return Browser(selenium)
