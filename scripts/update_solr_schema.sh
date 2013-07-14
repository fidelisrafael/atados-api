#!/bin/bash
ssh -t solr.atados '
sudo rm -rf /opt/solr/example/solr/conf/schema.xml
sudo wget https://raw.github.com/atados/atados/master/schema.xml -P /opt/solr/example/solr/conf/
'
