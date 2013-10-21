'''
Created on 20/09/2013

@author: mplanaguma
'''
from django.contrib.gis.geos import LineString, Point, MultiLineString, MultiPoint, LinearRing, Polygon
from opendai_lleida_web.models import GeoResolve
from opendai_client.geocoding_client import GeoCodingClient
from opendai_lleida_web.tasks import process_geocoding

import logging
import json
import utm
import sys

class GeoCodingLogic(object):


    def __init__(self):
        self.g_c = GeoCodingClient()
        
    
    def get_lat_lon_by_address_cached(self, address, bb=None):
        
        place = None
        lat = None
        lng = None
        
        try:
            geoResolved = GeoResolve.objects.get(address__exact=address)
            logging.debug( "Cached Place: " + geoResolved.place)
            return geoResolved.place, (float(geoResolved.lat), float(geoResolved.lng))
        
        except: 
            logging.info("No Cached Address: " + str(sys.exc_info()[0]))
            
            place, (lat, lng) = self.g_c.get_lat_lon_by_address(address, bb=bb)
            
            # Storing Cache 
            if place != None: 
                logging.debug( "Storing Place on DB: " + unicode(place)) 
                geoResolved = GeoResolve(address=address , place=place , lat=lat , lng=lng)
                try:
                    geoResolved.save()
                except:
                    logging.error("Storing error: " + sys.exc_info()[0]);
                
            return place, (lat, lng)
    
    
    def get_lat_lon_by_address_cached_async(self, address, bb=None):
        
        place = None
        lat = None
        lng = None
        
        try:
            geoResolved = GeoResolve.objects.get(address__exact=address)
            logging.debug( "Cached Place: " + geoResolved.place)
            return geoResolved.place, (float(geoResolved.lat), float(geoResolved.lng))
        
        except: 
            logging.info("No Cached Address: " + str(sys.exc_info()[0]))
            
            running_task = process_geocoding.apply_async(args=[address, bb])
            logging.debug("Async task: "+ running_task.id)
                
            return place, (lat, lng)        
        
    
    def get_lat_lon_by_street(self, street, city):
        return self.get_lat_lon_by_address_cached(street + ", " + city)


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
            
            
    def get_near(self, json, p_lat, p_lng, p_r):
        
        central_point = Point(p_lng, p_lat)
        
        circle = central_point.buffer(p_r/100000.0)
        #print circle.json
        
        points = []
        
        for o in json:
            lat = o['geo']['lat']
            lng = o['geo']['lng']
            if lat == None: continue
        
            point = Point( lng , lat)
            points.append(point)
        
        mp = MultiPoint(points)
        
        mp_results = mp.intersection(circle) 
        
        result = [mp_results.coords] if mp_results.geom_type == 'Point' else [coord for coord in mp_results.coords]
        return result
    
    
    def geocoding_cache(self, result_all):
        
        for index, item in enumerate(result_all):  
            
            street = item['street']
            place, (lat, lng) = self.geocoder.get_lat_lon_by_street(street, city)
        
        pass
        
        
        