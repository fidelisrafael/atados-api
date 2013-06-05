#!/bin/bash
source /opt/python/run/venv/bin/activate
. /opt/python/current/env 
python2.6 /opt/python/current/app/manage.py rebuild_index
deactivate
