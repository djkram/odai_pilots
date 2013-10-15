# -*- coding: utf-8 -*-
# BCN views 

from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render_to_response
from opendai_bcn_web.models import Pollution
from bs4 import BeautifulSoup
import datetime
import requests
import geojson
import json
import os
import re

#import datetime
#import logging
#from shapely.geometry import asShape
#from opendai_client.api_client import ApiClient
#from djgeojson.views import GeoJSONLayerView
#from opendai_bcn_web.models import TestGeo

from opendai_client.api_client import ApiClient

client = ApiClient()

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

def weather_all(request):
    
    result_all = client.get_bcn_weather_all()
    
    t_min, t_max, t_mati, t_tarda = None, None, None, None
    sym_moring= None
    sym_afternoon = None
    
    # Parsing: "Dc25-09: Temp.màx. 24 ºC Temp.mín. 18 ºC / Matí mig ennuvolat / Tarda mig ennuvolat"
    for o in result_all:
        d = o['description']
        
        p = "([0-9][0-9])-*"
        l = re.findall(p,d)
        
        t_day = l[0] # Dc25-09
        t_month = l[1] # Dc25-09
        t_max = l[2] # 24 ºC 
        t_min = l[3] # 18 ºC

        
        if int(t_day) == datetime.datetime.today().day and int(t_month) == datetime.datetime.today().month:
            link = o['link']
            path = link.replace(link.split('/')[-1],'')
            r  = requests.get(link)
            soup = BeautifulSoup(r.text)
            div_content =  soup.find(id="FW_content")
            imgs = div_content.find_all('img')
            link.split('/')[-1]
            sym_moring = path + str(imgs[0]['src'])
            sym_afternoon = path + imgs[1]['src']
            break
        else:
            continue
        
    result = {"max": t_max, "min": t_min, "prediction":{"morning": sym_moring, "afternoon": sym_afternoon}}
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result), mimetype, st)

#===============================================================================
# class TestGeoLayer(GeoJSONLayerView):
#    model = TestGeo
#    fields = ('title', 'datetime',)
#    # Options
#    srid = 4326     # projection
#    precision = 4   # float
#    simplify = 0.5  # generalization
#===============================================================================