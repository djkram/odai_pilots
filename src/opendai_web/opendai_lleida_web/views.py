# Lleida views 

import datetime, json
from django.http import HttpResponse
from django.shortcuts import render_to_response

from opendai_client.api_client import ApiClient

client = ApiClient()

def index(request):
    return render_to_response('lleida.html')

def alerts(request):
    
    result_all = client.get_lleida_alerts()
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def alerts_by_day(request, days="10"):
    
    result_all = client.get_lleida_alerts_days(days)
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)
    

def buslines_lines_geojson(request):
    
    result_all = client.get_lleida_buslines_all()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def bustops_all(request):
    
    result_all = client.get_lleida_bustops_all()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def bustops_by_id(request, id):
    
    result_all = client.get_lleida_bustops_id(id)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def pois_category_all(request):
    
    result_all = client.get_lleida_pois_categories_all()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def pois_by_category_id(request, id):
    
    result_all = client.get_lleida_pois_by_category_ids(id)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def accessibility_all(request):
    
    result_all = client.get_lleida_accessibility_all()
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def accessibility_id(request, id):
    
    result_all = client.get_lleida_accessibility_by_id(id)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def accessibility_category_id(request, id):
    
    result_all = client.get_lleida_accessibility_by_category_id(id)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def accessibility_feature_id(request, id):
    
    result_all = client.get_lleida_accessibility_by_feature_id(id)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

def accessibility_level_id(request, id):
    
    result_all = client.get_lleida_accessibility_by_level_id(id)
    
    st = 200
    mimetype = 'application/json'
    return HttpResponse(json.dumps(result_all), mimetype, st)

