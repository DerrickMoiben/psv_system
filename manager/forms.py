from . models import Route, Stage, Car
from django import forms


class ManagerSingupForm(forms.Form):
    username = forms.CharField(max_length=100)
    fullname = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class ManagerLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


