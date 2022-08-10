from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Passaword'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
