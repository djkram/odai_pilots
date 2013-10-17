'''
Created on 16/10/2013

@author: mplanaguma
'''
import datetime

from celery import task
from celery.task.schedules import crontab
from celery.task import periodic_task

from opendai_bcn_web.bcn_jobs import pollution_job

import logging

@task(name='process_pollution')
def process_pollution():
    logging.info("Pollution task executed!")
    pollution_job.get_pollution()
    return True

@periodic_task(run_every=datetime.timedelta(hours=12))
def cron_process_pollution():
    logging.info("Periodic Pollution task executed!")
    pollution_job.get_pollution()
    return True