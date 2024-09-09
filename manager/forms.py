from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . models import  Route, Stage, Car
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ManagerSingupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ManagerLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RouteForm(forms.ModelForm):
    stage = forms.ModelMultipleChoiceField(queryset=Stage.objects.all(), label="Select Stages", help_text="Choose one or more stages for this route.", widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Route
        fields = ['route_name',  'route_distance', 'route_price', 'stage']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['stage_name', 'stage_location']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_plate', 'seating_capacity', 'route']
