# -*- coding: utf-8 -*-
# BCN views 

from bs4 import BeautifulSoup
from celery.events.state import State
from celery.result import AsyncResult
from celery.task.control import inspect
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render_to_response
from opendai_bcn_web.bcn_jobs import *
from opendai_bcn_web.models import Pollution, Traffic
from opendai_bcn_web.tasks import *
from opendai_client.api_client import ApiClient
from opendai_client.shape_files import shapefiles
import geojson
import json
import logging
import os
import re
import requests

#import datetime
#import logging
#from shapely.geometry import asShape
#from opendai_client.api_client import ApiClient
#from djgeojson.views import GeoJSONLayerView
#from opendai_bcn_web.models import TestGeo

client = ApiClient()

def index(request):
    return render_to_response('bcn.html')

def pollution_geojson(request):

    # On demand
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

def pollution_geojson_async(request):
    
    deprecate_date = timedelta (minutes = 10)
    
    q = shapefiles.bcn_geojson()
        
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
        
        for f in q.features:
            district = f.properties['District']
            
            d = Pollution.objects.filter(district=district).order_by('-datetime').latest()
            
            # Adding pollution Data
            f.properties['Pollution'] = model_to_dict(d)
        
    except ObjectDoesNotExist:
        # Empty DB
        pollution_job.get_pollution()
        
    json = geojson.dumps(q)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json, mimetype, st)


def pollution_historic(request):
    
    all = Pollution.objects.all().order_by('-datetime')
    
    result = {'historic' : []}
    
    for pollution in all:
        result['historic'].append({str(pollution.datetime) : model_to_dict(pollution)});
        
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result), mimetype, st)

def pollution_days(request):
    
    all_days = Pollution.objects.datetimes('datetime','day','DESC')
    
    result = {'days' : []}
    
    for day in all_days:
        result['days'].append(str(day));
        
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result), mimetype, st)

def weather_all(request):
    
    result_all = client.get_bcn_weather_all()
    
    t_min, t_max, t_mati, t_tarda = None, None, None, None
    sym_moring= None
    sym_afternoon = None
    
    # Parsing: "Dc25-09: Temp.màx. 24 ºC Temp.mín. 18 ºC / Matí mig ennuvolat / Tarda mig ennuvolat"
    #        p = "([0-9][0-9])-*"
    #    l = re.findall(p,d)
    #    
    #    p2 = '(?<=..)\w+'
    #    l2 = re.findall(p2,d)
    #    
    #    t_day = l[0] # Dc25-09
    #    t_month = l[1] # Dc25-09
    #    t_max = l2[5] # 24 ºC 
    #    t_min = l2[10] # 18 ºC
    
    for o in result_all:
        
        t = o['title']
        
        if t == "min_max_temp":
            d = o['description']
            d_list = d.split()
            t_max = d_list[0]
            t_min = d_list[2]
        
        if t == "morning_link":
            sym_moring = o['link']
            
        if t == "afternoon_link":
            sym_afternoon = o['link']
        
        
    result = {"max": t_max, "min": t_min, "prediction":{"morning": sym_moring, "afternoon": sym_afternoon}}
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result), mimetype, st)


def traffic_lines_geojson(request):
    
    # Get traffic on demand
    traffic_job.get_trafic()
    result_all = client.get_bcn_traffic_current_geojson()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def traffic_lines_geojson_async(request):
    
    deprecate_date = timedelta (minutes = 10)
    
    try:
        last = Traffic.objects.all().latest()
        
        dt = last.datetime.replace(tzinfo=None) # Remove time zone
        # Celery task inspector
        celery_inspector = inspect()
        workers = celery_inspector.active()
        name, value = workers.popitem()
    
        if not last: # Empty Cache
            running_task = process_traffic.apply_async()
            logging.info('runing task: ' + running_task.id)
            
        elif ((datetime.datetime.utcnow() - dt) > deprecate_date) and not value: # Deprecated Cache
            running_task = process_traffic.apply_async()
            logging.info('runing task: ' + running_task.id)
    
    except ObjectDoesNotExist:
        # Get traffic on demand
        traffic_job.get_trafic()
    
    result_all = client.get_bcn_traffic_current_geojson_async()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)


def traffic_days(request):
    
    all_days = Traffic.objects.datetimes('datetime','day','DESC')
    
    result = {'days' : []}
    
    for day in all_days:
        result['days'].append(str(day));
        
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