#!/bin/bash
set -e

DJANGO_SETTINGS_MODULE=mmpp_conf.settings.production

LOGFILE=~/logs/mmpp_service-celery-stdout.log
LOGFILEERR=~/logs/mmpp_service-celery-stderr.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3

# user/group to run as
USER=c2020
GROUP=c2020
cd ~/C2020Clustering/mmpp_service
source ../env/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR
exec python manage.py celery worker -l INFO 2>>$LOGFILEERR