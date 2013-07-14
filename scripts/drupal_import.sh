#!/bin/bash
ssh -t ec2.atados '
if [ ! -d atados-migration-master ]; then
  wget https://github.com/atados/atados-migration/archive/master.zip
  unzip master
  rm -rf master
fi

if [ ! -d /home/ec2-user/atados ]; then
  ln -s /opt/python/current/app/ /home/ec2-user/atados
fi

source /opt/python/run/venv/bin/activate
. /opt/python/current/env 
python2.6 atados-migration-master/manage.py migratevolunteers --settings=atadosmigration.settings
python2.6 atados-migration-master/manage.py migratenonprofits --settings=atadosmigration.settings
python2.6 atados-migration-master/manage.py migrateprojects --settings=atadosmigration.settings
deactivate
'
