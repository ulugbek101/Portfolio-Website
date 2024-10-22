from django import forms
from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['address', 'profile_photo', 'rate', 'body']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'name',
                'placeholder': 'Ex: Brooklyn, NY, USA',
            }),
            'body': forms.Textarea(attrs={
                'placeholder': 'Some very cool review here ...'
            })
        }
