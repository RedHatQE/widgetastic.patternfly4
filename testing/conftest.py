import os
import subprocess
from urllib.request import urlopen

import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from wait_for import wait_for
from widgetastic.browser import Browser


CAPABILITIES = {
    "firefox": DesiredCapabilities.FIREFOX,
    "chrome": {
        **DesiredCapabilities.CHROME,
        "chromeOptions": {"args": ["disable-dev-shm-usage", "no-sandbox"]},
    },
}


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        help="name of the browser",
        choices=("firefox", "chrome"),
        default="firefox",
    )

    parser.addoption("--force-host", default=None, help="force a selenium hostname")


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return os.environ.get("BROWSER") or pytestconfig.getoption("--browser-name")


@pytest.fixture(scope="session")
def selenium_url(pytestconfig, worker_id):
    forced_host = pytestconfig.getoption("--force-host")

    if forced_host is None:
        oktet = 1 if worker_id == "master" else int(worker_id.lstrip("gw")) + 1
        host = f"127.0.0.{oktet}"
        ps = subprocess.run(
            [
                "podman",
                "run",
                "--rm",
                "-d",
                "-p",
                f"{host}:4444:4444",
                "-p",
                f"{host}:5999:5999",
                "--shm-size=2g",
                "quay.io/redhatqe/selenium-standalone:latest",
            ],
            stdout=subprocess.PIPE,
        )

        yield f"http://{host}:4444/wd/hub"
        container_id = ps.stdout.decode("utf-8").strip()
        subprocess.run(["podman", "kill", container_id], stdout=subprocess.DEVNULL)
    else:
        yield f"http://{forced_host}:4444/wd/hub"


@pytest.fixture(scope="session")
def wait_for_selenium(selenium_url):
    wait_for(lambda: urlopen(selenium_url), timeout=180, handle_exception=True)


@pytest.fixture(scope="module")
def selenium(browser_name, wait_for_selenium, selenium_url):
    driver = webdriver.Remote(
        command_executor=selenium_url, desired_capabilities=CAPABILITIES[browser_name.lower()]
    )
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser(selenium, request):
    selenium.maximize_window()
    selenium.get(request.module.TESTING_PAGE_URL)
    return Browser(selenium)
