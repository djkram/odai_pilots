'''
Created on 25/07/2013

@author: bdigital_mob
'''
import random

from opendai_client.api_client import ApiClient
from opendai_bcn_web.models import Pollution

import logging

client = ApiClient()

def get_pollution():
    
    result_all = client.get_pollution_all()
    #print result_all
    
    for r in result_all:
        
        zone = r['id_zone']
        result_by_id = client.get_pollution_by_ID(zone)
        
        for r in result_by_id:
            
            if r['hour'] == 'Mitjana':
                
                districts = zone_to_districts(zone)
                
                for d in districts:
                    logging.info("storing result for district : " + d)
                    alert = alarm_level_fake(r)
                    logging.info( alert)
                    
                    p = Pollution(district= d, so2=r['so2'], no=r['no'], no2=r['no2'], o3=r['o3'], co=r['co'], pm10=r['pm10'], alert=alert)
                    p.save()
            
            
def zone_to_districts (zone):
    map_district_to_zones = {'01': 1, '02':2, '03': 7, '04': 4, '05': 3, '06': 3, '07': 5, '08': 5, '09': 5, '10': 6 }

    result = []

    for k in map_district_to_zones.keys():
        v = map_district_to_zones[k]
    
        if zone == v:
            result.append(k)
    
    return result;

def alarm_level(r):
    
    so2=float(r['so2']) if r['so2'] is not None else 0
    no=float(r['no']) if r['no'] is not None else 0
    no2=float(r['no2']) if r['no2'] is not None else 0
    o3=float(r['o3']) if r['o3'] is not None else 0
    co=float(r['co'].replace(',','.')) if r['co'] is not None else 0
    pm10=float(r['pm10']) if r['pm10'] is not None else 0
    
    if so2 > 350 or no > 240 or no2 > 240 or o3 > 180 or co > 10 or pm10 > 50 :
        return 2
    
    if so2 >= 201 or no >= 116 or no2 >= 116 or o3 >= 111 or co >= 7 or pm10 >= 36 :
        return 1 
    
    return 0

def alarm_level_fake(r):
    l = [0,1,2]
    random.shuffle(l)
    result = l[0]
    return result
