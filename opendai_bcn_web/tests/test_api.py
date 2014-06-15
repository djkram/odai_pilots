"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from opendai_bcn_web.models import Pollution
from opendai_bcn_web import views
from opendai_client.geocoding_logic import GeoCodingLogic
from opendai_client.api_client import ApiClient

import json

class BCNAPITest(TestCase):
    
#===============================================================================
#    def test_pollution(self):
#        c = DataLoad()   
#        c.get_pollution()
#        c.get_pollution()
#        
#        b = Pollution.objects.all()
#        print b.count()
#        
#        for o in b:
#            print o.district
# 
#        ds = Pollution.objects.filter(district='01')
#        for d in ds:
#            print "Query result: " + d.district + " " + d.no2 + " " + str(d.datetime)
#            
#        d = Pollution.objects.filter(district='01').order_by('-datetime').latest()
#        print "Query result: " + d.district + " " + d.no2 + " " + str(d.datetime)
#        
#        self.assertIsNotNone(b, 'Not stored!')
#        self.assertEqual(b.count(), 20, 'Not enough districts!')
#===============================================================================
        
    
    #===========================================================================
    # def test_traffic(self):
    #    c = ApiClient()
    #    result = c.get_bcn_traffic_current()
    #    
    #    self.assertIsNotNone(result, 'Not Result!')
    #===========================================================================
         
         
    def test_weather(self):
        
        result = views.weather_all(None)
        
        self.assertIsNotNone(result, 'Not Result!')
        
        o_result = json.loads(result.content)
        self.assertTrue(o_result['max'].isdigit(), 'no max parsed')
        self.assertTrue(o_result['min'].isdigit(), 'no max parsed')
        
    
        pass
        
        
