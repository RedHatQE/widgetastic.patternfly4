import os
import subprocess
from urllib.request import urlopen

import pytest
from selenium import webdriver
from wait_for import wait_for
from widgetastic.browser import Browser


OPTIONS = {"firefox": webdriver.FirefoxOptions(), "chrome": webdriver.ChromeOptions()}


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
                "quay.io/redhatqe/selenium-standalone:ff_91.8.0esr_chrome_101.0.4951.41",
            ],
            stdout=subprocess.PIPE,
        )

        yield f"http://{host}:4444"
        container_id = ps.stdout.decode("utf-8").strip()
        subprocess.run(["podman", "kill", container_id], stdout=subprocess.DEVNULL)
    else:
        yield f"http://{forced_host}:4444"


@pytest.fixture(scope="session")
def wait_for_selenium(selenium_url):
    wait_for(lambda: urlopen(selenium_url), timeout=180, handle_exception=True)


@pytest.fixture(scope="session")
def selenium(browser_name, wait_for_selenium, selenium_url):
    driver = webdriver.Remote(command_executor=selenium_url, options=OPTIONS[browser_name.lower()])
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser(selenium, request):
    selenium.get(request.module.TESTING_PAGE_URL)
    yield Browser(selenium)
    selenium.refresh()
