"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from opendai_client.geocoding_client import GeoCodingClient
from opendai_client.api_client import ApiClient
from opendai_client.geocoding_logic import GeoCodingLogic

class GeoTest(TestCase):
    
    def setUp(self):
        
        self.a_c = ApiClient()
        self.g_c = GeoCodingLogic()
    
    def test_geocodingn(self):
        
        print "Test Geocoding..."

        bus_all = self.a_c.get_lleida_buslines_all()
        
        geojson = self.g_c.get_bus_line_geojson(bus_all)
        self.assertIsNotNone(geojson, 'No Response! get_bus_line_geojson')
        
        lat_lng = self.g_c.convert_utm_to_lat_lng(305169.8, 4611117.6, 31, 'T')
        self.assertIsNotNone(lat_lng, 'No Response! convert_utm_to_lat_lng')
        
        obj = [{"coordX": "305169.8", "geo": {"lat": 41.62795229360017, "lng": 0.6611302166483837}, "id": 1, "coordY": "4611117.6", "name": "Av Ind\u00fastria P.503"}, {"coordX": "305327.3", "geo": {"lat": 41.3850639, "lng": 2.1734035}}]
        p_lat = 41.62795229360017
        p_lng = 0.6611302166483837
        p_r = 10000
        bustop_near = self.g_c.get_near(obj, p_lat, p_lng, p_r)
        self.assertEqual([(0.6611302166483837, 41.62795229360017)], bustop_near, "Error: different number of ponts than expected")

        pass
    
    def test_geocodingn_cache(self):
        
        bb_lleida = [(0.5599594116210938,41.580525125613846),(0.5599594116210938,41.65649719441145),(0.7123947143554688,41.65649719441145),(0.7123947143554688,41.580525125613846)]
        
        resolved = self.g_c.get_lat_lon_by_address_cached("major, Lleida", bb=bb_lleida)
        self.assertIsNotNone(resolved)
        resolved = self.g_c.get_lat_lon_by_address_cached("carrer major, Lleida")
        self.assertIsNotNone(resolved)
        
        resolved = self.g_c.get_lat_lon_by_address_cached("djhsbdvkjhasbdkjchv", bb=bb_lleida)
        self.assertIsNotNone(resolved)
        
        resolved = self.g_c.get_lat_lon_by_address_cached_async("djhsbdvkjhasbdkjchv", bb=bb_lleida)
        
        pass