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
    datetime = models.DateField(auto_now=True)

    class Meta:
        get_latest_by = 'datetime'
    
    