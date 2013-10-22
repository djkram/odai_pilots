# -*- coding: utf-8 -*-
'''
Created on 17/10/2013

@author: mplanaguma
'''

from celery import task
from celery.task import periodic_task
from opendai_client.geocoding_client import GeoCodingClient
from opendai_lleida_web.models import GeoResolve
import datetime, sys
import logging

geocoder = GeoCodingClient()

@task(name='process_geocoding')
def process_geocoding(address, bb):
    logging.info("Geocoding task executed by address: " + address)
    
    result = geocoder.get_lat_lon_by_address(address, bb=bb)
    
    prefix_list = ['Carrer ', 'Plaça ', 'Via ', 'Passeig ', 'Avinguda ', 'Av. ', 'Carretera ']
    if not result:
        
        for prefix in prefix_list:
            logging.info("Trying with prefix: " + prefix)
            prefix_address = prefix + address
            result = geocoder.get_lat_lon_by_address(prefix_address, bb=bb)
            if result:
                break
    
    place, (lat, lng) = result

    # Storing Cache 
    if place: 
        logging.info( "Storing Place on DB: " + unicode(place)) 
        geoResolved = GeoResolve(address=address , place=place , lat=lat , lng=lng)
        try:
            geoResolved.save()
        except:
            logging.error("Storing error: " + str(sys.exc_info()[1]));
                
    return True