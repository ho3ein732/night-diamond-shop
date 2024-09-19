from django import forms
from .models import ReturnedItem, ReturnImage
from django.forms import modelformset_factory


class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnedItem
        fields = [
            'reason',
            'email',
            'phone'
        ]


class ReturnImageForm(forms.ModelForm):
    class Meta:
        model = ReturnImage
        fields = [
            'image'
        ]


ReturnImageFormset = modelformset_factory(ReturnImage,form=ReturnImageForm, extra=3)

