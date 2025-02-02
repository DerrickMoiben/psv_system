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

# forms.py
from django import forms
from .models import Ticket, Stage, StagePrice

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['car', 'alighting_stage', 'name', 'phone_number', 'seat_number', 'payment_method']

    def __init__(self, *args, **kwargs):
        self.route = kwargs.pop('route', None)
        super().__init__(*args, **kwargs)
        
        if self.route:
            # Filter cars assigned to this route
            self.fields['car'].queryset = self.route.cars.all()
            
            # Filter stages that have prices for this route
            valid_stages = Stage.objects.filter(
                id__in=StagePrice.objects.filter(route=self.route).values('stage_id')
            )
            self.fields['alighting_stage'].queryset = valid_stages
            print("Stages in form:", valid_stages)