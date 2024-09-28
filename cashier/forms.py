from django import forms
from django.contrib.auth.forms import UserCreationForm
from manager.models import CustomUser

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
from manager.models import Stage, Route, StagePrice

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'number', 'car', 'route', 'alighting_stage', 'price', 'seat_number', 'payment_method']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        
        if 'route' in self.data:
            try:
                route_id = int(self.data.get('route'))
                # Use routes__route_id instead of routes__id for filtering
                self.fields['alighting_stage'].queryset = Stage.objects.filter(routes__route_id=route_id)
            except (ValueError, TypeError):
                self.fields['alighting_stage'].queryset = Stage.objects.none()
        elif self.instance.pk:
            # If editing an existing instance, get related stages
            self.fields['alighting_stage'].queryset = self.instance.route.stage_set.all()

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