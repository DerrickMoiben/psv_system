from django.db import models

# Create your models here.    

class City(models.Model):
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name

class Stage(models.Model):
    stage_name = models.CharField(max_length=50)
    stage_location = models.CharField(max_length=50)
    city_name = models.ForeignKey(City, on_delete=models.CASCADE, null=True, related_name='stages')

    def __str__(self):
        return self.stage_name

class Route(models.Model):
    stage_name = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    route_name = models.ForeignKey(City, related_name='starting_routes', on_delete=models.CASCADE, null=True)
    route_start = models.ForeignKey(City, related_name='ending_routes', on_delete=models.CASCADE, null=True)
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
