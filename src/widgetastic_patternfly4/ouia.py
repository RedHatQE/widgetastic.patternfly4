import importlib
import sys

from widgetastic.utils import ParametrizedLocator


class OUIAMixin:

    ROOT = ParametrizedLocator(
        './/*[@data-ouia-component-type="PF4/{@component_type}" and '
        '@data-ouia-component-id="{@component_id}"]'
    )

    def __init__(self, component_type, component_id):
        self.component_type = component_type
        self.component_id = component_id

    @property
    def is_safe(self):
        return "true" in self.browser.get_attribute("data-ouia-safe", self)


class ImportHack:
    def __getattr__(self, name):
        if name.endswith("OUIA"):
            return self.generate_ouia_compat_widget(name)

    def generate_ouia_compat_widget(self, name):
        klass_name = name.rstrip("OUIA")
        module = importlib.import_module("widgetastic_patternfly4")
        klass = getattr(module, klass_name)
        if not hasattr(klass, "PF_NAME"):
            raise ImportError(f"{klass_name} is not OUIA ready")

        class WidgetWithOUIA(klass, OUIAMixin):
            def __init__(self, parent, component_id, logger=None, *args, **kwargs):
                klass.ROOT = OUIAMixin.ROOT
                OUIAMixin.__init__(self, klass.PF_NAME, component_id)
                super(klass, self).__init__(parent, logger=logger)

        WidgetWithOUIA.__name__ = WidgetWithOUIA.__qualname__ = name
        return WidgetWithOUIA


sys.modules[__name__] = ImportHack()
