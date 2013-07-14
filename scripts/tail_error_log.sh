#!/bin/bash
ssh -t ec2.atados '
sudo tail -f /var/log/httpd/error_log
'
