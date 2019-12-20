from widgetastic.widget import View

from widgetastic_patternfly4 import BreadCrumb


def test_breadcrumb(browser):
    class TestView(View):
        ROOT = ".//main[@role='main']"
        breadcrumb = BreadCrumb()

    view = TestView(browser)
    assert view.breadcrumb.is_displayed
    assert len(view.breadcrumb.locations) == 4
    assert view.breadcrumb.locations[0].lower() == "section home"
    assert view.breadcrumb.read().lower() == "section landing"
    view.breadcrumb.click_location(view.breadcrumb.locations[0])
