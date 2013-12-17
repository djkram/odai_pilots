'''
Created on 16/12/2013

@author: mplanaguma
'''

from opendai_client.api_client import ApiClient
import datetime
import logging
from opendai_bcn_web.models import Noise


client = ApiClient()


def get_noise_map():
    
    all_streets = client.get_streets_all()
    
    for street in all_streets:
        
        id_street = street['id_street'] 
        type_street = street['type']
        street_long_name = street['official_name']
        street_short_name = street['name18']
        
        for number in xrange(0,100,5):
        
            print street_long_name + ", " + str(number)
            noise_street = client.get_noise(street_long_name, str(number))
            print noise_street
    
            if noise_street:
                
                noise_morning = noise_street['morning']
                noise_evening = noise_street['evening']
                noise_night = noise_street['night']
                
                Noise(id_street=id_street,type_street=type_street,short_name_street=street_short_name,long_name_street=street_long_name,num_steet=number,noise_morning=noise_morning,noise_evening=noise_evening,noise_night=noise_night)
    
    pass