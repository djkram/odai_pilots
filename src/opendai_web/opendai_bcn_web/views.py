# BCN views 
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render_to_response
from opendai_bcn_web.models import Pollution
import geojson
import os

#import datetime
#import json
#import logging
#from shapely.geometry import asShape
#from opendai_client.api_client import ApiClient
#from djgeojson.views import GeoJSONLayerView
#from opendai_bcn_web.models import TestGeo

def index(request):
    return render_to_response('bcn.html')


def bcn_geojson(request):
    
    file_name = 'bcn.json'
    dir_name = os.path.dirname(__file__)
    full_path = os.path.join(dir_name, file_name)
    
    f = open(full_path,'r')
    json = f.read()
    #print json
    
    q = geojson.loads(json, object_hook=geojson.GeoJSON.to_instance)
    
    for f in q.features:
        district = f.properties['District']
        
        d = Pollution.objects.filter(district=district).order_by('-datetime').latest()
        
        f.properties['Pollution'] = model_to_dict(d)
        
        print d.district
         
        #=======================================================================
        # zone = map_district_to_zones[district]
        # print zone
        # 
        # result_by_id = client.get_pollution_by_ID(zone)
        # print result_by_id
        #=======================================================================
        
        #result_by_id.data.entry
        
    json = geojson.dumps(q)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json, mimetype, st)

#===============================================================================
# class TestGeoLayer(GeoJSONLayerView):
#    model = TestGeo
#    fields = ('title', 'datetime',)
#    # Options
#    srid = 4326     # projection
#    precision = 4   # float
#    simplify = 0.5  # generalization
#===============================================================================