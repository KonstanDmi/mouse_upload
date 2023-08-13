from django import forms
from .models import DirUploadModel



class MultipleFileInput(forms.ClearableFileInput): # Class for multiple selection in input
    allow_multiple_selected = True


class MultipleFileField(forms.FileField): # Class for field in form that works with multiple files when selected more then one file
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DirUploadForm(forms.Form):
    file = MultipleFileField(label='',)



# DirUploadFormSet = forms.modelformset_factory(model=DirUploadModel, form=DirUploadForm)
#tryed to do multiple selection by formsets, got confused