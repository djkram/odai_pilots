"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from opendai_bcn_web.bcn_jobs import traffic_job, noise_job, pollution_job
from opendai_bcn_web.models import Traffic, Noise, Pollution


class PollutionJobTest(TestCase):
    
    def setUp(self):
        pass
    
    def test_pollution_job(self):
        

        print "Test Pollution job..."

        pollution_job.get_pollution()
        last_pollution_stored = Pollution.objects.all().latest()
        
        self.assertIsNotNone(last_pollution_stored, 'Not Stored Pollution!')
        
        district = '1'
        d = Pollution.objects.filter(district=district).order_by('-datetime').latest()
        
        print d

        pass


class TrafficJobTest(TestCase):
    
    def setUp(self):
        pass
        
    
    def test_traffic_job(self):
        
        print "Test Traffic job..."

        traffic_job.get_trafic()
        last_traffic_stored = Traffic.objects.all().latest()
        
        self.assertIsNotNone(last_traffic_stored, 'Not Stored Traffic!')

        s_1 = len(Traffic.objects.all())
        traffic_job.get_trafic()
        s_2 = len(Traffic.objects.all())
        self.assertEqual(s_1, s_2, 'Control date not works')
        

        pass
  
class NoiseJobTest(TestCase):
    
    def setUp(self):
        pass  
  
    def test_noise_job(self):
        
        print "Test Noise job..." 
        
        noise_job.get_noise_map()
        
        last_noise_stored = Noise.objects.all().latest()
        
        self.assertIsNotNone(last_noise_stored, 'Not Stored Traffic!')
        
        pass



class ComparationJobTest(TestCase):
    
    def setUp(self):
        pass  
  
    def test_job(self):
        
        
        
        pass