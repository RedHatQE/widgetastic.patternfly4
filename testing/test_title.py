from widgetastic.widget import View

from widgetastic_patternfly4 import Title


TESTING_PAGE_URL = "https://patternfly-react.surge.sh/components/title"


class TitleTestView(View):
    h1 = Title("4xl Title")
    h2 = Title("3xl Title")
    h3 = Title("2xl Title")
    h4 = Title("xl Title")
    h5 = Title("lg Title")
    h6 = Title("md Title")


def test_location_and_size(browser):
    view = TitleTestView(browser)
    for name in view.widget_names:
        widget = getattr(view, name)
        assert widget.is_displayed
        assert widget.text == widget.expected
        assert str(widget.heading_level) == str(name)
