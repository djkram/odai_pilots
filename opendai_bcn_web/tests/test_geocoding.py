"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from opendai_client.geocoding_client import GeoCodingClient
from opendai_client.api_client import ApiClient
from opendai_client.geocoding_logic import GeoCodingLogic
from opendai_bcn_web.bcn_jobs import traffic_job

class GeoTest(TestCase):
    
    def setUp(self):
        
        self.a_c = ApiClient()
        self.g_c = GeoCodingLogic()
    
    def test_traffic_cache(self):
        
        print "Test Geocoding..."

        traffic_job.get_trafic()
        self.g_c.get_traffic_geojson_async()

        pass
    
