#!/bin/bash

#1 Make dump from atadosco_portal
atados # Alias to cd into backend directory
mysqldump -u username -p -h remote.site.com DBNAME > atadosco_portal.sql

#2 drop schema public cascade; create schema public
psql -U marjoripomarole -d atados -c "drop schema public cascade; create schema public"

#3 Create table and import fixtures with Django
make install

#4 migrate time
migration # Alias to cd into migration directory
make migrate

# Wait and go eat something ....
