'''
Created on 23/10/2013

@author: mplanaguma
'''
import datetime, json, sys
import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response

from opendai_client.geocoding_logic import GeoCodingLogic

geocoder = GeoCodingLogic()

def geocoding(request):
    
    mimetype = 'application/json'
    
    try:
        street = request.GET.get('street')
        city = request.GET.get('city')
        bb_str = request.GET.get('bb', None)
        
        address = street +  ", " + city
        
        logging.info('address=' +  address)
        
        bb = None
        try: 
            bb_list = bb_str.split(',')
            bb = [(bb_list[0],bb_list[1]),(bb_list[2],bb_list[3]),(bb_list[4],bb_list[5]),(bb_list[6],bb_list[7]),(bb_list[0],bb_list[1])]
        except:
            logging.warning('Error creating BB')
            # Default Lleida
            #bb = [(0.5599594116210938,41.580525125613846),(0.5599594116210938,41.65649719441145),(0.7123947143554688,41.65649719441145),(0.7123947143554688,41.580525125613846)]
         
        place, (lat, lng) = geocoder.get_lat_lon_by_address_cached(address, bb)
        
        result = []
        if place:
            result = place, (lat, lng)

        st = 200
        return HttpResponse(json.dumps(result), mimetype, st)
    
    except :
        logging.warning(str(sys.exc_info()))
        st = 400
        return HttpResponse('400: Bad Request',st)    
    
   