'''
Created on 06/06/2013

@author: mplanaguma
'''
import unittest

from opendai_client.api_client import ApiClient

class Test(unittest.TestCase):

    client = None

    def setUp(self):
        
        self.client = ApiClient()
        pass


    def tearDown(self):
        pass


    def testPollution(self):
        
        result_all = self.client.get_pollution_all()
        print result_all
        
        self.assertIsNotNone(result_all[0])
        self.assertEqual(7, len(result_all), "error result number")
        
        for r in result_all:
            result_by_id = self.client.get_pollution_by_ID(r['id_zone'])
            print result_by_id
            
            #print result_by_id[0]['co']
            
            self.assertIsNotNone(result_by_id)
            
        pass
    
    '''
    def testPollen(self):
        
        result_all = self.client.get_pollen_all()
        print result_all
        
        self.assertIsNotNone(result_all[0])
        
        pass
    
    def testNoise(self):
        
        result_all = self.client.get_noise("roc boronat", "115")
        print result_all
        
        self.assertIsNotNone(result_all[0])
        
        pass
    '''

    def testBusStop(self):
        
        result_all = self.client.get_lleida_bustops_all()
        print result_all
        
        self.assertIsNotNone(result_all[0])
        
        for r in result_all:
            result_by_id = self.client.get_lleida_bustops_all(r['id'])
            print result_by_id
            
            self.assertIsNotNone(result_by_id)
            
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()