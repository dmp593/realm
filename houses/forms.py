import decimal
import shutil
import mimetypes

from pathlib import Path
from urllib.parse import unquote

from django import forms
from django.conf import settings
from django.core.files.storage import default_storage

from houses.models import House, HouseFile
from houses.widgets import FilePreviewWidget, FilePreviewInlineWidget

LEN_MEDIA_URL = len(settings.MEDIA_URL)


class DecimalToIntegerField(forms.IntegerField):
    def prepare_value(self, value):
        if isinstance(value, decimal.Decimal):
            return int(value)

        return value


class HouseForm(forms.ModelForm):
    price_in_euros = DecimalToIntegerField(min_value=0, required=True)
    discount_in_euros = DecimalToIntegerField(min_value=0, required=False)

    class Meta:
        model = House
        fields = '__all__'


class HouseFileForm(forms.ModelForm):
    file = forms.FileField(widget=FilePreviewWidget, required=False)
    tmp_file = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = HouseFile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        tmp_file = self.cleaned_data.get('tmp_file')

        if tmp_file:
            if self.instance.file and default_storage.exists(self.instance.file.name):
                default_storage.delete(self.instance.file.name)

            tmp_file = Path(default_storage.location).joinpath(unquote(tmp_file)[LEN_MEDIA_URL:])

            self.instance.filename = tmp_file.name
            self.instance.content_type = mimetypes.guess_type(self.instance.filename)[0]

            with open(tmp_file, 'rb') as f:
                self.instance.file.save(self.instance.filename, f)

            shutil.rmtree(tmp_file.parent)

        return super().save(commit)


class HouseFileInlineForm(HouseFileForm):
    file = forms.FileField(widget=FilePreviewInlineWidget, required=False)
