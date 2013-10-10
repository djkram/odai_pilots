"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from opendai_bcn_web.data_cron import DataCron
from opendai_bcn_web.models import Pollution


class SimpleTest(TestCase):
    
    def test_basic_addition(self):
        c = DataCron()   
        c.get_pollution()
        c.get_pollution()
        
        b = Pollution.objects.all()
        print b.count()
        
        #=======================================================================
        # for o in b:
        #    print o.district
        #=======================================================================

        ds = Pollution.objects.filter(district='01')
        for d in ds:
            print "Query result: " + d.district + " " + d.no2 + " " + str(d.datetime)
            
        d = Pollution.objects.filter(district='01').order_by('-datetime').latest()
        print "Query result: " + d.district + " " + d.no2 + " " + str(d.datetime)
        
        self.assertIsNotNone(b, 'Not stored!')
        self.assertEqual(b.count(), 20, 'Not enough districts!')
         
        
