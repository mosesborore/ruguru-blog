from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Account


class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email/userename', required=True)
