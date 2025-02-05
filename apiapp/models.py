from django.db import models


class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lattitude = models.FloatField()
    lon = models.FloatField()
    temp_c = models.FloatField()
    temp_color = models.CharField(max_length=7)
    wind_kph = models.FloatField()
    wind_color = models.CharField(max_length=7)
    cloud = models.IntegerField()
    cloud_color = models.CharField(max_length=7)
    timestamp = models.DateTimeField(auto_now_add=True)