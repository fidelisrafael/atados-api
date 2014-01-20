#!/bin/bash

# Make dump from atadosco_portal
source ~/.virtualenvs/atados/bin/activate
cd ~/projects/atados/atados
mysqldump -u atadosco_master -p -h atados.com.br atadosco_portal > atadosco_portal.sql # This might take a few minutes...

# Restore the backup locally
mysql -u root atadosco_portal -e "drop database atadosco_portal; create database atadosco_portal;"
mysql -u root atadosco_portal < atadosco_portal.sql

# Clean local new psql database
psql -U marjoripomarole -d atados -c "drop schema public cascade; create schema public"

# Create tables and import fixtures with Django
make install

#4 migrate time
cd ~/projects/atados/atados-migration
make migrate

# Wait and go eat something ....

# make dump and restore remotely on rds
pg_dump dbname=atados -f atados.sql
psql -f atados.sql --host=atadosdb.cnpn2qkpvnvn.sa-east-1.rds.amazonaws.com --port=5432 --username=atadosdb --password --dbname=atadosdb
