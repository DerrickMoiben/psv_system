from django.db import models


# Create your models here.    

class Stage(models.Model):
    stage_name = models.CharField(max_length=50)
    stage_location = models.CharField(max_length=50)
    def __str__(self):
        return self.stage_name

class Route(models.Model):
    stage = models.ManyToManyField(Stage, related_name='routes')
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=50)
    route_distance = models.IntegerField()
    def __str__(self):
        return self.route_name
    

class Car(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='cars')
    car_plate = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    def __str__(self):
        return self.car_plate

class StagePrice(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stage_prices')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='stage_prices')
    price = models.IntegerField()

    class Meta:
        unique_together = ('route', 'stage')

    def __str__(self):
        return f'{self.route} - {self.stage}'
    


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)