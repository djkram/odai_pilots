'''
Created on 15/10/2013

@author: mplanaguma
'''
import os
import geojson

def bcn_geojson():
    
    file_name = 'bcn.json'
    dir_name = os.path.dirname(__file__)
    full_path = os.path.join(dir_name, file_name)
    
    f = open(full_path,'r')
    json = f.read()
    #print json
    
    bcn_geojson = geojson.loads(json, object_hook=geojson.GeoJSON.to_instance)
    
    return bcn_geojson