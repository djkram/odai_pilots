"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from opendai_bcn_web.bcn_jobs import traffic_job
from opendai_bcn_web.models import Traffic


class JobTest(TestCase):
    
    def setUp(self):
        pass
        
    
    def test_traffic_job(self):
        
        print "Test Geocoding..."

        traffic_job.get_trafic()
        last_traffic_stored = Traffic.objects.all().latest()
        
        self.assertIsNotNone(last_traffic_stored, 'Not Stored Traffic!')

        s_1 = len(Traffic.objects.all())
        traffic_job.get_trafic()
        s_2 = len(Traffic.objects.all())
        self.assertEqual(s_1, s_2, 'Control date not works')
        

        pass
    
