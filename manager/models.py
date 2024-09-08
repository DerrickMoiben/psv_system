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
    route_id = models.AutoField(primary_key=True)
    start_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='start_stage')
    end_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='end_stage')
    route_name = models.CharField(max_length=50)
    route_start_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='starting_routes')
    route_end_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ending_routes')
    route_distance = models.IntegerField()
    route_price = models.IntegerField()

    def __str__(self):
        return self.route_name
    

class Car(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='cars')
    car_plate = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    stages_pickup = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='pickup_stages')
    stages_dropoff = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='dropoff_stages')

    def __str__(self):
        return self.car_plate
