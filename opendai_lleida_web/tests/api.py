"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from opendai_client.api_client import ApiClient

class APITest(TestCase):
    
    def test_api(self):
        
        print "Test API..."

        a_c = ApiClient()
        
        bus_all = a_c.get_lleida_buslines_all()
        self.assertIsNotNone(bus_all, 'No Response! get_lleida_buslines_all')
        
        bustop_all = a_c.get_lleida_bustops_all()
        self.assertIsNotNone(bustop_all, 'No Response! get_lleida_bustops_all')
        
        p_lat = 41.62795229360017
        p_lng = 0.6611302166483837
        p_r = 10000
       
        bustop_near = a_c.get_lleida_bustops_near(p_lat, p_lng, p_r)
        self.assertNotEqual(bustop_all, bustop_near, "Sema that general search")
        
        #alert_all = a_c.get_lleida_alerts()
        #self.assertIsNotNone(alert_all, 'No Response! get_lleida_alerts')
        