'''
Created on 20/09/2013

@author: mplanaguma
'''
from django.contrib.gis.geos import LineString, Point, MultiLineString
from geopy import geocoders
from opendai_lleida_web.models import GeoResolve
import logging
import json
import geojson
import utm
import sys

class GeoCoding(object):


    def __init__(self):
        self.g_geonames = geocoders.GeoNames()
        self.g_google = geocoders.GoogleV3()
        
        
    def get_lat_lon_by_address(self, address):
        
        place = None
        lat = None
        lng = None
        
        try:
            geoResolved = GeoResolve.objects.get(address__exact=address)
            logging.debug( "Cached Place: " + geoResolved.place)
            return geoResolved.place, (float(geoResolved.lat), float(geoResolved.lng))
        
        except: 
            logging.warn("Finding error: " + sys.exc_info()[0])
            # try Geonames api
            try:  
                logging.debug( "Georesolving GeoNames"    )   
                geo_result = self.g_geonames.geocode(address)
                if geo_result != None:
                    place, (lat, lng) = geo_result[0], (geo_result[1][0], geo_result[1][1])
            except:
                logging.warn( "GeoNames Oops!")
                
            # try google api
            if place == None:
                try:
                    logging.debug( "Georesolving Google Maps 1"  )
                    place, (lat, lng) = self.g_google.geocode(address)
                except:
                    try:
                        logging.debug( "Georesolving Google Maps 2" ) 
                        place, (lat, lng) = self.g_google.geocode("carrer " + address)   
                    except:  
                        logging.warn( "Google Oops!")  
            
            # Storing Cache 
            if place != None: 
                logging.debug( "Storing Place on DB: " + str(place)) 
                geoResolved = GeoResolve(address=address , place=place , lat=lat , lng=lng)
                try:
                    geoResolved.save()
                except:
                    logging.error("Storing error: " + sys.exc_info()[0]);
                
            return place, (lat, lng)
    
    
    def get_lat_lon_by_street(self, street, city):
        return self.get_lat_lon_by_address(street + ", " + city)


    def get_bus_line_geojson(self, jsons):
        
        line_geojson = {}
        fc = {"type": "FeatureCollection", "features": []}
        
        for j in jsons:
            
            bus_line_name = None
            try: 
                bus_line_name = str(j.get('description'))
            except:
                continue
            
            lists = line_geojson.get(bus_line_name, None)
            if lists == None:
                lists = []
            
            line = []
                
            points = [x.replace("0 ", "") for x in j.get('coordinates').split(',')]
            for position in xrange(len(points)/2):
                p = position * 2
                point = Point( float(points[p]) , float(points[p+1]))
                line.append(point)
            
            lstr = LineString(line)
            lists.append(lstr)
                
            line_geojson[str(j.get('description'))] = lists
        
        for line, list in line_geojson.iteritems():
            f = { "type": "Feature", "geometry": {}, "properties": {} }
            mlstr = MultiLineString(list)
            ml_geojson = mlstr.json
            f["geometry"] = json.loads(ml_geojson)
            f["properties"] = {"bus_line": line}
            fc["features"].append(f)
            
        return fc
    
    
    def convert_utm_to_lat_lng(self, x, y, zone_number, zone_letter):
        try:
            return utm.to_latlon(x, y, zone_number, zone_letter)  
        except:
            return (None, None)
            
            
        
        