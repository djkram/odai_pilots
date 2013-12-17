from django.db import models
#from django.contrib.gis.db import models


#===============================================================================
# class TestGeo(models.Model):
#    title = models.CharField(max_length=30)
#    datetime = models.DateField()
#    #point = models.PointField()
#===============================================================================

class Pollution(models.Model):
    district = models.CharField(max_length=20)
    so2 = models.CharField(max_length=20, null=True)
    no = models.CharField(max_length=20, null=True)
    no2 = models.CharField(max_length=20, null=True)
    o3 = models.CharField(max_length=20, null=True)
    co = models.CharField(max_length=20, null=True)
    pm10 = models.CharField(max_length=20, null=True)
    # 0-Good 1-Bad 2-Poor
    alert = models.IntegerField()
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'datetime'
    
    
class Traffic(models.Model):
    id_stretch = models.CharField(max_length=10, unique_for_date='datetime')
    description = models.CharField(max_length=1000, null=True)
    coordinates = models.CharField(max_length=5000, null=False)
    status = models.CharField(max_length=10, null=False)
    forecast = models.CharField(max_length=10, null=False)
    tstamp = models.CharField(max_length=20, null=False)
    
    datetime = models.DateTimeField()

    class Meta:
        get_latest_by = 'datetime'
        

class Noise(models.Model):
    id_street = models.CharField(max_length=10, unique_for_date='datetime')
    type_street = models.CharField(max_length=10, null=True)
    short_name_street = models.CharField(max_length=1000, null=True)
    long_name_street = models.CharField(max_length=1000, null=False)
    num_street = models.CharField(max_length=10, null=False)
    noise_morning = models.CharField(max_length=20, null=False)
    noise_evening = models.CharField(max_length=20, null=False)
    noise_night = models.CharField(max_length=20, null=False)
    
    datetime = models.DateTimeField()

    class Meta:
        get_latest_by = 'datetime'
    