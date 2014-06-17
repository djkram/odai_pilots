#!/bin/bash
set -e

DJANGO_SETTINGS_MODULE=admin_web.settings-production

LOGFILE=/var/log/opendai/django_stdout.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3

# user/group to run as
USER=root
GROUP=root
cd /var/www/odai_pilots
#source ../env/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn admin_web.wsgi:application -w $NUM_WORKERS \
	--user=$USER --group=$GROUP --log-level=info \
    --log-file=$LOGFILE -b 0.0.0.0:8001 2>>$LOGFILE