'''
Created on 16/10/2013

@author: mplanaguma
'''
import datetime

from celery import task
from celery.task.schedules import crontab
from celery.task import periodic_task

from opendai_bcn_web.bcn_jobs import pollution_job, traffic_job

import logging

@task(name='process_pollution')
def process_pollution():
    logging.info("Pollution task executed!")
    pollution_job.get_pollution()
    return True

@periodic_task(run_every=datetime.timedelta(minutes=30))
def cron_process_pollution():
    logging.info("Periodic Pollution task executed!")
    pollution_job.get_pollution()
    return True

@task(name='process_traffic')
def process_traffic():
    logging.info("Traffic task executed!")
    traffic_job.get_trafic()
    return True

@periodic_task(run_every=datetime.timedelta(minutes=15))
def cron_process_traffic():
    logging.info("Periodic Traffic task executed!")
    traffic_job.get_trafic()
    return True
