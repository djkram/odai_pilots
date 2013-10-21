'''
Created on 17/10/2013

@author: mplanaguma
'''
import datetime, sys

from celery import task
from celery.task import periodic_task

from opendai_client.geocoding_client import GeoCodingClient
from opendai_lleida_web.models import GeoResolve


import logging

geocoder = GeoCodingClient()

@task(name='process_geocoding_all')
def process_geocoding_all(result_all):
    logging.info("Geocoding task executed!")
    
    bb_lleida = [(0.5599594116210938,41.580525125613846),(0.5599594116210938,41.65649719441145),(0.7123947143554688,41.65649719441145),(0.7123947143554688,41.580525125613846)]
    
    for index, p in enumerate(result_all): 
        street = p['street']
        
        address = street + ", Lleida"
        
        place, (lat, lng) = geocoder.get_lat_lon_by_address(address, bb=bb_lleida)
    
        # Storing Cache 
        if place != None: 
            logging.debug( "Storing Place on DB: " + unicode(place)) 
            geoResolved = GeoResolve(address=address , place=place , lat=lat , lng=lng)
            try:
                geoResolved.save()
            except:
                logging.error("Storing error: " + sys.exc_info()[0]);
                
    return True

@task(name='process_geocoding')
def process_geocoding(address, bb):
    logging.info("Geocoding task executed!")
    
    place, (lat, lng) = geocoder.get_lat_lon_by_address(address, bb=bb)

    # Storing Cache 
    if place != None: 
        logging.debug( "Storing Place on DB: " + unicode(place)) 
        geoResolved = GeoResolve(address=address , place=place , lat=lat , lng=lng)
        try:
            geoResolved.save()
        except:
            logging.error("Storing error: " + sys.exc_info()[0]);
                
    return True