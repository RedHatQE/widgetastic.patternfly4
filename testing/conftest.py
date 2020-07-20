import os
import subprocess
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from wait_for import wait_for_decorator
from widgetastic.browser import Browser


@pytest.fixture(scope="session")
def browser_name():
    return os.environ["BROWSER"]


@pytest.fixture(scope="session")
def selenium_port(worker_id):
    s_port = 4444 + int(worker_id.lstrip("gw"))
    ps = subprocess.run(
        [
            "sudo",
            "podman",
            "run",
            "--rm",
            "-d",
            "-p",
            f"{s_port}:4444",
            "--shm-size=2g",
            "quay.io/redhatqe/selenium-standalone",
        ],
        stdout=subprocess.PIPE,
    )
    yield s_port
    container_id = ps.stdout.decode("utf-8").strip()
    subprocess.run(["sudo", "podman", "kill", container_id])


@pytest.fixture(scope="session")
def wait_for_port(selenium_port):
    @wait_for_decorator(timeout=10, handle_exception=True)
    def make_request():
        urlopen(f"http://127.0.0.1:{selenium_port}/wd/hub")


@pytest.fixture(scope="module")
def selenium(browser_name, wait_for_port, selenium_port):
    command_executor = f"http://127.0.0.1:{selenium_port}/wd/hub"
    if browser_name == "firefox":
        driver = webdriver.Remote(
            command_executor=command_executor, desired_capabilities=DesiredCapabilities.FIREFOX
        )
    elif browser_name == "chrome":
        caps = DesiredCapabilities.CHROME.copy()
        caps["chromeOptions"] = {"args": ["disable-dev-shm-usage", "no-sandbox"]}
        driver = webdriver.Remote(command_executor=command_executor, desired_capabilities=caps)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser(selenium, request):
    name = request.module.__name__.split("_")[1]
    category = getattr(request.module, "CATEGORY", "components")
    url = f"https://patternfly-react.surge.sh/documentation/react/{category}/{name}"
    selenium.maximize_window()
    selenium.get(url)
    return Browser(selenium)
