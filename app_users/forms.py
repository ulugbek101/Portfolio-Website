from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from . import models

User = get_user_model()


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


class RegistrationForm(UserCreationForm):
    """Manual sign-up: username, email, optional names and a password pair."""

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={"class": "field", "placeholder": _("you@example.com")}),
    )
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        widget=forms.TextInput(attrs={"class": "field", "placeholder": _("Optional")}),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        widget=forms.TextInput(attrs={"class": "field", "placeholder": _("Optional")}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "field", "placeholder": _("Username")}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "field", "placeholder": _("Password")}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "field", "placeholder": _("Confirm password")}
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("An account with this email already exists."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Edit personal information, avatar and newsletter preference."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "headline", "location", "avatar", "newsletter")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "field"}),
            "last_name": forms.TextInput(attrs={"class": "field"}),
            "email": forms.EmailInput(attrs={"class": "field"}),
            "headline": forms.TextInput(attrs={"class": "field"}),
            "location": forms.TextInput(attrs={"class": "field"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if email and qs.exists():
            raise forms.ValidationError(_("An account with this email already exists."))
        return email
