from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . models import City, Route, Stage, Car
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
        fields = ['route_name', 'route_start_city', 'route_end_city', 'route_distance', 'route_price']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['stage_name', 'stage_location']


class CarForm(forms.ModelForm):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), required=True)
    stages_pickup = forms.ModelChoiceField(queryset=Stage.objects.all(), required=True)
    stages_dropoff = forms.ModelChoiceField(queryset=Stage.objects.all(), required=True)
    
    class Meta:
        model = Car
        fields = ['car_plate', 'seating_capacity', 'route', 'stages_pickup', 'stages_dropoff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stages_pickup'].queryset = Stage.objects.none()
        self.fields['stages_dropoff'].queryset = Stage.objects.none()

        if 'route' in self.data:
            try:
                route_id = int(self.data.get('route'))
                self.fields['stages_pickup'].queryset = Stage.objects.filter(route__id=route_id).order_by('stage_name')
                self.fields['stages_dropoff'].queryset = Stage.objects.filter(route__id=route_id).order_by('stage_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['stages_pickup'].queryset = self.instance.route.start_stage_set.order_by('stage_name')
            self.fields['stages_dropoff'].queryset = self.instance.route.end_stage_set.order_by('stage_name')

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city_name']