from django.db import models

# Create your models here.

class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=50)
    route_start = models.CharField(max_length=50)
    route_end = models.CharField(max_length=50)
    route_distance = models.IntegerField()
    route_price = models.IntegerField()

class Stage(models.Model):
    stage_name = models.CharField(max_length=50)
    stage_location = models.CharField(max_length=50)


class Car(models.Model):
    car_plate = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    