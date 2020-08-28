import sys

from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import GenericLocatorWidget
from widgetastic.widget import Table
from widgetastic.widget import Widget
from widgetastic.xpath import quote

import widgetastic_patternfly4
from .dropdown import Dropdown


class OUIAMixin:

    ROOT = ParametrizedLocator(
        ".//*[@data-ouia-component-type={@component_type} and "
        "@data-ouia-component-id={@component_id}]"
    )

    def __init__(self, component_type, component_id):
        self.component_type = quote(f"PF4/{component_type}")
        self.component_id = quote(component_id)
        self.locator = self.ROOT.locator

    @property
    def is_safe(self):
        return "true" in self.browser.get_attribute("data-ouia-safe", self)


def generate_ouia_compat_class(name):
    klass_name = name.rstrip("OUIA")
    try:
        klass = getattr(widgetastic_patternfly4, klass_name)
    except AttributeError:
        raise ImportError(f"cannot import name '{klass_name}'")
    if not hasattr(klass, "PF_NAME"):
        raise ValueError(f"{klass_name} is not OUIA ready")

    class WidgetWithOUIA(OUIAMixin, klass):
        def __init__(self, parent, component_id, logger=None, *args, **kwargs):
            OUIAMixin.__init__(self, klass.PF_NAME, component_id)
            if issubclass(klass, GenericLocatorWidget):
                super(klass, self).__init__(parent, self.locator, logger=logger)
            elif issubclass(klass, Table):
                super(klass, self).__init__(parent, self.locator, logger=logger, **kwargs)
            elif issubclass(klass, Dropdown):
                Widget.__init__(self, parent, logger=logger)
            else:
                super(klass, self).__init__(parent, logger=logger)

    WidgetWithOUIA.__name__ = WidgetWithOUIA.__qualname__ = name
    return WidgetWithOUIA


class WidgetsClassesCache(dict):
    def __missing__(self, key):
        klass = generate_ouia_compat_class(key)
        self[key] = klass
        return klass


class ImportHack:

    cache = WidgetsClassesCache()
    objs = {name: getattr(sys.modules[__name__], name) for name in dir(sys.modules[__name__])}

    def __getattr__(self, name):
        if name.endswith("OUIA"):
            return self.cache[name]
        if name == "__path__":
            return
        if name == "__all__":
            return [key for key in self.objs.keys()]
        return self.objs[name]


sys.modules[__name__] = ImportHack()
