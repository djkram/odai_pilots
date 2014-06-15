#!/bin/bash
set -e

DJANGO_SETTINGS_MODULE=admin_web.settings.production

LOGFILE=/var/log/opendai/django_console.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3

# user/group to run as
USER=root
GROUP=root
cd /var/www/odai_pilots
#source ../env/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR
exec python2.7 manage.py celery worker -B -l INFO 2>>$LOGFILE