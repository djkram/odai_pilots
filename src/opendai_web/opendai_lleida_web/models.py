from django.db import models

# Create your models here.


class GeoResolve(models.Model):
    address = models.CharField(max_length=200, unique=True)
    place = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=30, decimal_places=20)
    lng = models.DecimalField(max_digits=30, decimal_places=20)