from django.db import models
from manager.models import Car, StagePrice

# Create your models here.

# cashier/models.py
from django.db import models
from manager.models import Car, Stage, Route, StagePrice
from django.conf import settings

class Ticket(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='tickets')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tickets')
    boarding_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='boarding_tickets')
    alighting_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='alighting_tickets')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seat_number = models.IntegerField()
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket {self.id} for Route {self.route.route_name}'

    class Meta:
        unique_together = ('car', 'seat_number', 'created_at')  # Ensure seat uniqueness per car
