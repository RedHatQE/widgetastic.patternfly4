from widgetastic.ouia import OUIAGenericView
from widgetastic.ouia import OUIAGenericWidget
from widgetastic.widget.table import Table
from widgetastic.xpath import quote

from widgetastic_patternfly4.alert import BaseAlert
from widgetastic_patternfly4.breadcrumb import BaseBreadCrumb
from widgetastic_patternfly4.button import BaseButton
from widgetastic_patternfly4.contextselector import BaseContextSelector
from widgetastic_patternfly4.dropdown import BaseDropdown
from widgetastic_patternfly4.dropdown import BaseGroupDropdown
from widgetastic_patternfly4.dropdown import BaseSplitButtonDropdown
from widgetastic_patternfly4.formselect import BaseFormSelect
from widgetastic_patternfly4.modal import BaseModal
from widgetastic_patternfly4.navigation import BaseNavigation
from widgetastic_patternfly4.optionsmenu import BaseOptionsMenu
from widgetastic_patternfly4.pagination import BaseCompactPagination
from widgetastic_patternfly4.pagination import BasePagination
from widgetastic_patternfly4.select import BaseCheckboxSelect
from widgetastic_patternfly4.select import BaseSelect
from widgetastic_patternfly4.switch import BaseSwitch
from widgetastic_patternfly4.table import BaseExpandableTable
from widgetastic_patternfly4.table import BasePatternflyTable


class Alert(BaseAlert, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/Alert"


class BreadCrumb(BaseBreadCrumb, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/Breadcrumb"


class Button(BaseButton, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/Button"


class Dropdown(BaseDropdown, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/Dropdown"


class GroupDropdown(BaseGroupDropdown, Dropdown):
    pass


class SplitButtonDropdown(BaseSplitButtonDropdown, Dropdown):
    pass


class FormSelect(BaseFormSelect, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/FormSelect"


class Modal(BaseModal, OUIAGenericView):
    OUIA_COMPONENT_TYPE = "PF4/ModalContent"


class Navigation(BaseNavigation, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/Nav"


class Pagination(BasePagination, OUIAGenericView):
    OUIA_COMPONENT_TYPE = "PF4/Pagination"


class CompactPagination(BaseCompactPagination, Pagination):
    pass


class CheckboxSelect(BaseCheckboxSelect, Dropdown):
    OUIA_COMPONENT_TYPE = "PF4/Select"


class Switch(BaseSwitch, OUIAGenericWidget):
    OUIA_COMPONENT_TYPE = "PF4/Switch"


class PatternflyTable(BasePatternflyTable, Table):
    def __init__(
        self,
        parent,
        component_id,
        column_widgets=None,
        assoc_column=None,
        rows_ignore_top=None,
        rows_ignore_bottom=None,
        top_ignore_fill=False,
        bottom_ignore_fill=False,
        logger=None,
    ):
        self.component_type = "PF4/Table"
        self.component_id = component_id
        super().__init__(
            parent,
            locator=(
                f".//*[@data-ouia-component-type={quote(self.component_type)} "
                f"and @data-ouia-component-id={quote(self.component_id)}]"
            ),
            column_widgets=column_widgets,
            assoc_column=assoc_column,
            rows_ignore_top=rows_ignore_top,
            rows_ignore_bottom=rows_ignore_bottom,
            top_ignore_fill=top_ignore_fill,
            bottom_ignore_fill=bottom_ignore_fill,
            logger=logger,
        )


class ExpandableTable(BaseExpandableTable, PatternflyTable):
    pass


class Select(BaseSelect, Dropdown):
    OUIA_COMPONENT_TYPE = "PF4/Select"


class ContextSelector(BaseContextSelector, Select):
    OUIA_COMPONENT_TYPE = "PF4/ContextSelector"


class OptionsMenu(BaseOptionsMenu, Dropdown):
    OUIA_COMPONENT_TYPE = "PF4/OptionsMenu"
