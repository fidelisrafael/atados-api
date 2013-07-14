#!/bin/bash
wget https://github.com/atados/atados-migration/archive/master.zip
unzip master
ln -s /opt/python/current/app/ /home/ec2-user/atados
source /opt/python/run/venv/bin/activate
. /opt/python/current/env 
python2.6 atados-migration-master/manage.py migratevolunteers --settings=atadosmigration.settings
python2.6 atados-migration-master/manage.py migratenonprofits --settings=atadosmigration.settings
python2.6 atados-migration-master/manage.py migrateprojects --settings=atadosmigration.settings
deactivate
