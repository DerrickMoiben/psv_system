from django.db import models
from manager.models import Car, Stage, Route, StagePrice
from django.conf import settings

class Ticket(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Mpesa', 'Mpesa'),
    ]
    ticket_id = models.CharField(max_length=100, unique=True, editable=True, default='T1905251')
    name = models.CharField(max_length=100, default='name')
    phone_number = models.CharField(max_length=100, default='0')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='tickets')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tickets')
    alighting_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='alighting_tickets')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seat_number = models.IntegerField()
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket {self.id} for Route {self.route.route_name}'

    class Meta:
        unique_together = ('car', 'seat_number', 'created_at')  # Ensure seat uniqueness per car
