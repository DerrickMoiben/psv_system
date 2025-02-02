from django import forms
from django.contrib.auth.forms import UserCreationForm
from manager.models import CustomUser, Route


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name']
        
class RouteSelectionForm(forms.Form):
    route = forms.ModelChoiceField(queryset=Route.objects.all(), empty_label='Select a route')
    
    
class CashierSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'cashier'  # Set the role to cashier
        if commit:
            user.save()
        return user


from django import forms
from .models import Ticket
from manager.models import Stage, Route, StagePrice, Car

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['car', 'alighting_stage', 'phone_number', 'name', 'payment_method', 'seat_number']

    def __init__(self, *args, **kwargs):
        route = kwargs.pop('route', None)
        super().__init__(*args, **kwargs)
        
        if route:
            # Filter vehicles assigned to this route
            self.fields['car'].queryset = route.cars.all()
            
            # Filter stages available for this route
            self.fields['alighting_stage'].queryset = Stage.objects.filter(
                stage_prices__route=route
            ).distinct()
