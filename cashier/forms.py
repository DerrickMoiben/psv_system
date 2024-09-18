from django import forms
from .models import Ticket
from manager.models import Route, Stage, StagePrice

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'number', 'car', 'route', 'boarding_stage', 'alighting_stage', 'price', 'seat_number', 'payment_method']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        # Initialize the fields with data
        if 'route' in self.data:
            try:
                route_id = int(self.data.get('route'))
                self.fields['boarding_stage'].queryset = Stage.objects.filter(routes__id=route_id)
                self.fields['alighting_stage'].queryset = Stage.objects.filter(routes__id=route_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['boarding_stage'].queryset = self.instance.route.stage_set.all()
            self.fields['alighting_stage'].queryset = self.instance.route.stage_set.all()

    def clean(self):
        cleaned_data = super().clean()
        route = cleaned_data.get('route')
        boarding_stage = cleaned_data.get('boarding_stage')
        alighting_stage = cleaned_data.get('alighting_stage')

        if route and boarding_stage and alighting_stage:
            # Fetch the price for the selected stages
            try:
                stage_price = StagePrice.objects.get(route=route, stage=alighting_stage)
                cleaned_data['price'] = stage_price.price
            except StagePrice.DoesNotExist:
                raise forms.ValidationError("Price for the selected stage is not defined.")
        
        return cleaned_data
