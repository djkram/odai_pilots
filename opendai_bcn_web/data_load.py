'''
Created on 25/07/2013

@author: mplanaguma
'''
import time
import random
import threading
import multiprocessing

from opendai_bcn_web.bcn_jobs import pollution_job
from apscheduler.scheduler import Scheduler

#from opendai_bcn_web.bcn_jobs.pollution_job import PollutionJob

class DataLoad(threading.Thread):
    '''
    classdocs
    '''
    client = None

    def __init__(self, my_id):
        # Init Loading
        super(DataLoad, self).__init__(name=my_id)
        self.my_id = my_id
        
        # Scheduling
        #self.sched = Scheduler()
        #self.sched.add_interval_job(pollution_job.get_pollution(),minutes=1)
        #self.sched.start()
        

    def run(self):
        print "Start Running Pollution"
        pollution_job.get_pollution()
        print "End Running Pollution"
        return