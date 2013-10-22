'''
Created on 20/09/2013

@author: mplanaguma
'''
from django.contrib.gis.geos import LineString, Point, MultiLineString, MultiPoint, LinearRing, Polygon
from geopy import geocoders

import logging, sys

class GeoCodingClient(object):


    def __init__(self):
        self.g_geonames = geocoders.GeoNames()
        self.g_google = geocoders.GoogleV3()
        self.g_bing = geocoders.Bing('Aoouq4D8UL3y9_QmnkA67qP7xvBiDVXWsMZbQ1OPlXWupph9AcA39Z2kltMawU2J')
        #Pending
        #geocoders.MediaWiki()
        #geocoders.SemanticMediaWiki()
        #geocoders.MapQuest()
        #geocoders.OpenMapQuest()
#        geocoders.Yahoo()
        
    def get_lat_lon_by_address(self, address, bb=None):
        
        if bb:
            l_box = LinearRing(bb[0],bb[1],bb[2],bb[3],bb[0])
            bounding_box = Polygon(l_box)
        
        place = None
        lat = None
        lng = None
        
        def is_inside(geo_results,bounding_box):
            if geo_results:
                for geo_result in geo_results:
                        p_place, (p_lat, p_lng) = geo_result[0], (geo_result[1][0], geo_result[1][1])
                        p_candidate = Point(float(p_lng),float(p_lat))
                        inside = bounding_box.contains(p_candidate)
                        if inside:
                            return p_place, (p_lat, p_lng)
            return None, (None, None)
        
        # try Geonames api
        try:  
            logging.debug( "Georesolving GeoNames")   
            if bb:
                geo_results = self.g_geonames.geocode(address, exactly_one=False)
                place, (lat, lng) = is_inside(geo_results, bounding_box)
            else:
                geo_result = self.g_geonames.geocode(address, exactly_one=True)
                if geo_result:
                    place, (lat, lng) = geo_result
            
        except:
            logging.warn( "GeoNames Exception: " + str(sys.exc_info()[1]))
            
        # try google api
        if place == None:
            try:
                logging.debug( "Georesolving Google Maps"  )
                if bb:
                    geo_results = self.g_google.geocode(address, region="es", exactly_one=False)
                    place, (lat, lng) = is_inside(geo_results, bounding_box)
                else:
                    place, (lat, lng) = self.g_google.geocode(address, region="es", exactly_one=True)
                
            except:
                logging.warn( "Google Exception: " + str(sys.exc_info()[1]))  
                
        # try Bing api
        if place == None:
            try:
                logging.debug( "Georesolving Bing Maps"  )
                
                if bb:
                    geo_results = self.g_bing.geocode(address, exactly_one=False)
                    place, (lat, lng) = is_inside(geo_results, bounding_box)
                else:
                    place, (lat, lng) = self.g_bing.geocode(address, exactly_one=False)
                
            except:
                logging.warn( "Bing Exception: " + str(sys.exc_info()[1]))  
                
        return place, (lat, lng)
    
