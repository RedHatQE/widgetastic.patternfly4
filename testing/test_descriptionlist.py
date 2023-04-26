import pytest
from widgetastic.widget import View

from widgetastic_patternfly4 import DescriptionList


TESTING_PAGE_URL = "https://patternfly-react-main.surge.sh/components/description-list"


@pytest.fixture(scope="module")
def view(browser):
    class TestView(View):
        ROOT = ".//div[@id='ws-react-c-description-list-basic']"
        description_list = DescriptionList()

    return TestView(browser)


def test_description_list_is_displayed(view):
    assert view.description_list.is_displayed


def test_description_list_items(view):
    expected_res = {
        "Name": "Example",
        "Namespace": "mary-test",
        "Labels": "example",
        "Pod selector": "app=MyApp",
        "Annotation": "2 Annotations",
    }
    assert view.description_list.read() == expected_res
