import os

import pytest
from selenium import webdriver
from widgetastic.browser import Browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(scope="session")
def browser_name():
    return os.environ["BROWSER"]


@pytest.fixture(scope="module")
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
    elif browser_name == "remote_firefox":
        driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX)
    elif browser_name == "remote_chrome":
        caps = DesiredCapabilities.CHROME.copy()
        caps["chromeOptions"] = {"args": ["disable-dev-shm-usage", "no-sandbox"]}
        driver = webdriver.Remote(desired_capabilities=caps)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser(selenium, request):
    name = request.module.__name__.split("_")[1]
    category = getattr(request.module, "CATEGORY", "components")
    url = "https://patternfly-react.surge.sh/patternfly-4/{}/{}/?shadow=false"
    selenium.maximize_window()
    selenium.get(url.format(category, name))
    return Browser(selenium)
