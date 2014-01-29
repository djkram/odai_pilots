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

def calculate():
    
    t_now = datetime.datetime.now().replace(tzinfo=utc)
    period = datetime.datetime.timedelta(hours=1)

    Traffic.objects.filter()

    pass            
        
