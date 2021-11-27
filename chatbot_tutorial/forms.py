from django import forms
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=6)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError("The 2 passwords do not match")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=6)
    password = forms.CharField(widget=forms.PasswordInput())
