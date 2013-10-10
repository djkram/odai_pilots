"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from opendai_client.geocoding_client import GeoCoding
from opendai_client.api_client import ApiClient

class SimpleTest(TestCase):
    
    def test_basic_addition(self):

        a_c = ApiClient()
        g_c = GeoCoding()
        
        bus_all = a_c.get_lleida_buslines_all()
        self.assertIsNotNone(bus_all, 'No Response! get_lleida_buslines_all')
        
        geojson = g_c.get_bus_line_geojson(bus_all)
        self.assertIsNotNone(geojson, 'No Response! get_bus_line_geojson')
        
        lat_lng = g_c.convert_utm_to_lat_lng(305169.8, 4611117.6, 31, 'T')
        print lat_lng
        self.assertIsNotNone(lat_lng, 'No Response! convert_utm_to_lat_lng')
        
        bustop_all = a_c.get_lleida_bustops_all()
        self.assertIsNotNone(bustop_all, 'No Response! get_lleida_bustops_all')