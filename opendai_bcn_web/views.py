# -*- coding: utf-8 -*-
# BCN views 

from bs4 import BeautifulSoup
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render_to_response
from opendai_bcn_web.models import Pollution
from opendai_client.api_client import ApiClient
from opendai_client.shape_files import shapefiles

from datetime import datetime, timedelta
import geojson
import json
import os
import logging
import re
import requests
from celery.events.state import State
from celery.task.control import inspect
from celery.result import AsyncResult
from django.core.exceptions import ObjectDoesNotExist

from opendai_bcn_web.tasks import *
from opendai_bcn_web.bcn_jobs import *
#import datetime
#import logging
#from shapely.geometry import asShape
#from opendai_client.api_client import ApiClient
#from djgeojson.views import GeoJSONLayerView
#from opendai_bcn_web.models import TestGeo

client = ApiClient()

def index(request):
    return render_to_response('bcn.html')


def bcn_geojson(request):
    
    deprecate_date = timedelta (seconds = 1)
    try:
        last = Pollution.objects.all().latest()
        
        dt = last.datetime.replace(tzinfo=None) # Remove time zone
        # Celery task inspector
        celery_inspector = inspect()
        workers = celery_inspector.active()
        name, value = workers.popitem()
    
        if not last: # Empty Cache
            pollution_job.get_pollution()
            
        elif ((datetime.datetime.utcnow() - dt) > deprecate_date) and not value: # Deprecated Cache
            running_task = process_pollution.apply_async()
            #print "Running task"
            logging.debug(running_task.ready())
        
    except ObjectDoesNotExist:
        # Empty DB
        pollution_job.get_pollution()
        

    
    q = shapefiles.bcn_geojson()
    
    for f in q.features:
        district = f.properties['District']
        
        d = Pollution.objects.filter(district=district).order_by('-datetime').latest()
        
        # Adding pollution Data
        f.properties['Pollution'] = model_to_dict(d)
        
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


def traffic_lines_geojson(request):
    
    running_task = process_traffic.apply_async()
    logging.info('runing task: ' + running_task.id)
    result_all = client.get_bcn_traffic_current_geojson()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def traffic_lines_geojson_async(request):
    
    result_all = client.get_bcn_traffic_current_geojson_async()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

#===============================================================================
# class TestGeoLayer(GeoJSONLayerView):
#    model = TestGeo
#    fields = ('title', 'datetime',)
#    # Options
#    srid = 4326     # projection
#    precision = 4   # float
#    simplify = 0.5  # generalization
#===============================================================================