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
def selenium_host(worker_id):
    oktet = 1 if worker_id == "master" else int(worker_id.lstrip("gw")) + 1
    host = f"127.0.0.{oktet}"
    # we have to run a rootful container due to https://github.com/containers/podman/issues/7016
    # TODO remove sudo when the bug will be fixed
    ps = subprocess.run(
        [
            "sudo",
            "podman",
            "run",
            "--rm",
            "-d",
            "-p",
            f"{host}:4444:4444",
            "--shm-size=2g",
            "quay.io/redhatqe/selenium-standalone",
        ],
        stdout=subprocess.PIPE,
    )
    yield host
    container_id = ps.stdout.decode("utf-8").strip()
    subprocess.run(["sudo", "podman", "kill", container_id])


@pytest.fixture(scope="session")
def wait_for_selenium(selenium_host):
    @wait_for_decorator(timeout=10, handle_exception=True)
    def make_request():
        urlopen(f"http://{selenium_host}:4444/wd/hub")


@pytest.fixture(scope="module")
def selenium(browser_name, wait_for_selenium, selenium_host):
    command_executor = f"http://{selenium_host}:4444/wd/hub"
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
