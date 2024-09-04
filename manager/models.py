from django.db import models

# Create your models here.    
class Stage(models.Model):
    stage_name = models.CharField(max_length=50)
    stage_location = models.CharField(max_length=50)

    def __str__(self):
        return self.stage_name

class Route(models.Model):
    stage_name = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True) 
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=50)
    route_start = models.CharField(max_length=50)
    route_end = models.CharField(max_length=50)
    route_distance = models.IntegerField()
    route_price = models.IntegerField()

    def __str__(self):
        return self.route_name



class Car(models.Model):
    route_name = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    car_plate = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    
    def __str__(self):
        return self.car_plate
