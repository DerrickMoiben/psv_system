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
        fields = ['name', 'phone_number', 'car', 'alighting_stage', 'price', 'seat_number', 'payment_method']

    def __init__(self, *args, **kwargs):
        route = kwargs.pop('route', None)  # Get the route passed from the view
        super(TicketForm, self).__init__(*args, **kwargs)

        if route:
            # Filter alighting stages based on the selected route
            self.fields['alighting_stage'].queryset = Stage.objects.filter(routes=route)
            # Filter cars based on the selected route (assuming a relationship exists)
            self.fields['car'].queryset = Car.objects.filter(route=route)  # Adjust this line based on your model relationships
        else:
            self.fields['alighting_stage'].queryset = Stage.objects.none()
            self.fields['car'].queryset = Car.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        route = cleaned_data.get('route')
        alighting_stage = cleaned_data.get('alighting_stage')

        if route and alighting_stage:
            try:
                stage_price = StagePrice.objects.get(route=route, stage=alighting_stage)
                cleaned_data['price'] = stage_price.price
            except StagePrice.DoesNotExist:
                raise forms.ValidationError("Price for the selected stage is not defined.")

        return cleaned_data
