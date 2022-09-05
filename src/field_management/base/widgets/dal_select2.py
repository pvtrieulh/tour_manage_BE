from django.forms.widgets import Media
from django import forms
from dal_select2.widgets import Select2WidgetMixin, QuerySetSelectMixin, Select, SelectMultiple


class Select2WidgetMixinBase(Select2WidgetMixin):
    """ use for widget extend, not use in app """
    @property
    def media(self):
        return Media()


class AutocompleteModelSelect2Base(
    QuerySetSelectMixin,
    Select2WidgetMixinBase,
    forms.Select
):
    """ use for widget of form, with select single, ex:
    class OrderAdminForm(Select2AdminForm):
        class Meta:
            widgets = {
                'col_name': AutocompleteModelSelect2Base(url='company:select2-search-ajax-tn'),
            }
    """
    pass


class AutocompleteModelMultiSelect2Base(
    QuerySetSelectMixin,
    Select2WidgetMixinBase,
    forms.SelectMultiple
):
    """ use for widget of form, with select multi, ex:
    class OrderAdminForm(Select2AdminForm):
        class Meta:
            widgets = {
                'col_name': AutocompleteModelMultiSelect2Base(url='company:select2-search-ajax-tn'),
            }
    """
    pass


class AutocompleteSelect2(Select2WidgetMixinBase, Select):
    """ use for widget of form, with select data fix defined, ex:
    class OrderAdminForm(Select2AdminForm):
        class Meta:
            widgets = {
                'col_name': AutocompleteSelect2(),
            }
    """
    pass


class AutocompleteSelect2Multiple(Select2WidgetMixinBase, SelectMultiple):
    """ use for widget of form, with multi select data fix defined, ex:
    class OrderAdminForm(Select2AdminForm):
        class Meta:
            widgets = {
                'col_name': AutocompleteSelect2Multiple(),
            }
    """
    pass


class Select2AdminForm(forms.ModelForm):
    """ use for form, extend form, ex:
    class OrderAdminForm(Select2AdminForm):
        class Meta:
            widgets = {
                'col_name': AutocompleteModelMultiSelect2Base(url='company:select2-search-ajax-tn'),
            }
    """
    @property
    def media(self):
        return forms.ModelForm.media.fget(self) + Select2WidgetMixin().media
