#!/bin/bash
ssh -t ec2.atados '
source /opt/python/run/venv/bin/activate
. /opt/python/current/env 
python2.6 /opt/python/current/app/manage.py createsuperuser
deactivate
'
