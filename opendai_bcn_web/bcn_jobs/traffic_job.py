'''
Created on 25/07/2013

@author: mplanaguma
'''

from django.utils.timezone import utc
from opendai_bcn_web.models import Traffic
from opendai_client.api_client import ApiClient
import datetime
import logging


client = ApiClient()

def get_trafic():

    # change TZ info
    t_now = datetime.datetime.now().replace(tzinfo=utc)
    traffic_status = client.get_bcn_traffic_current()
    
    try:
        last_traffic_stored = Traffic.objects.all().latest()
        
        if traffic_status[0]['tstamp'] == last_traffic_stored.tstamp:
            # Not new Data
            logging.info("Not New traffic data to store, ts: " + traffic_status[0]['tstamp'])
            return
        
    except:
        logging.info("Not stored traffic")
        
    
    for index, t_s in enumerate(traffic_status): 
        
        id = t_s['id']
        s_r = client.get_streets_stretches_by_id(id)
        logging.debug('Got street stretch: ' + id)
        
        try:
            description = s_r[0]['description']
            coordinates = s_r[0]['coordinates']
            status = t_s['status']
            forecast = t_s['forecast']
            tstamp = t_s['tstamp']
            
            t = Traffic(id_stretch=id, description=description, coordinates=coordinates, status=status, forecast=forecast, tstamp=tstamp, datetime=t_now)
            t.save()
            
        except Exception, e:
            logging.warning(e)
            
        
