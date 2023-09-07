# pylint: disable=E5142
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    # meta dados para o form
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
