from widgetastic.widget import View

from widgetastic_patternfly4 import Title


TESTING_PAGE_URL = "https://patternfly-react-main.surge.sh/components/title"


class TitleTestView(View):
    h1 = Title("h1 defaults to 2xl")
    h2 = Title("h2 defaults to xl")
    h3 = Title("h3 defaults to lg")
    h4 = Title("h4 defaults to md")
    h5 = Title("h5 defaults to md")
    h6 = Title("h6 defaults to md")


def test_location_and_size(browser):
    view = TitleTestView(browser)
    for name in view.widget_names:
        widget = getattr(view, name)
        assert widget.is_displayed
        assert widget.text == widget.expected
        assert str(widget.heading_level) == str(name)
