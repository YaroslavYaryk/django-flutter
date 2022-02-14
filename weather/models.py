from pyexpat import model
from django.db import models
from django.forms import FloatField

# Create your models here.


class Weather(models.Model):

    day = models.IntegerField()
    time = models.CharField(max_length=50)
    temperature = models.FloatField()
    wind_direction = models.CharField(max_length=50)
    wind_speed = models.FloatField()
    weather_kod = models.CharField(max_length=20)
    cloud_number = models.IntegerField()

    def __str__(self) -> str:
        return f"day={self.day}, time={self.time}"


class UsedFiles(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True,
                            verbose_name="URL",
                            null=True,
                            )

    def __str__(self):
        return self.name
