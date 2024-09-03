from . models import Route, Stage, Car
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
    class Meta:
        model = Route
        fields = ['route_name', 'route_start', 'route_end', 'route_distance', 'route_price']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['stage_name', 'stage_location']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_plate', 'seating_capacity']

