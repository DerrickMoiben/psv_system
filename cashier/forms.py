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


# cashier/forms.py
from django import forms
from .models import Ticket
from manager.models import Stage, Car

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['route', 'car', 'boarding_stage', 'alighting_stage', 'seat_number']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['route'].queryset = Car.objects.none()  # Start with no cars loaded
        self.fields['boarding_stage'].queryset = Stage.objects.none()  # Start with no stages
        self.fields['alighting_stage'].queryset = Stage.objects.none()

        # Route is dynamically loaded based on user input in the view
