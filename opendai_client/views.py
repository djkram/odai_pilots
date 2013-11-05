'''
Created on 23/10/2013

@author: mplanaguma
'''
import datetime, json
from django.http import HttpResponse
from django.shortcuts import render_to_response

from opendai_client.geocoding_logic import GeoCodingLogic

geocoder = GeoCodingLogic()

def geocoding(request):
    
    mimetype = 'application/json'
    
    try:
        address = request.GET.get('address')
        bb = request.GET.get('bb', None)
        
        result_all = geocoder.get_lat_lon_by_address_cached(address, bb)

        st = 200
        return HttpResponse(json.dumps(result_all), mimetype, st)
    
    except :
        st = 400
        return HttpResponse('400: Bad Request',st)    
    
   