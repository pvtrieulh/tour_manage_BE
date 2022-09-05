import collections
from dal import autocomplete
from django import forms
from .choices import *
from .models import Option


class BaseForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_STANDARD)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BaseForm, self).__init__(*args, **kwargs)

        try:
            op = Option.objects.get(user_id=self.request.user.id)
            if op.option == SUPERUSER:
                self.fields['status'].choices = STATUS_ADVANCED
            if op.option == SUPEREDITOR:
                self.fields['status'].choices = STATUS_STANDARD
            if op.option == EDITOR:
                self.fields['status'].choices = STATUS_EDITOR
        except Option.DoesNotExist:
            self.fields['status'].choices = STATUS_STANDARD


class VoiceInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        try:
            arr_voices = []
            for ele in self.cleaned_data:
                if not ele['DELETE']:
                    arr_voices.append(ele['accent'])

            for item, count in collections.Counter(arr_voices).items():
                if count > 1:
                    raise forms.ValidationError("Giọng đọc bị trùng")

        except (AttributeError, KeyError):
            return


class VoiceInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VoiceInlineForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.accent in OLD_ACCENT:
            self.fields['accent'].disabled = True
        else:
            self.fields['accent'].choices = GOOGLE_ACCENT
