#!/bin/sh

/etc/init.d/elasticsearch start
/etc/init.d/postgresql start
#python /atados-api/manage.py migrate

#python /atados-api/manage.py runserver 0.0.0.0:8000 &
#cd /atados-www && grunt serve &
