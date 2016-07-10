#!/usr/bin/env bash

set -xe
serv=httpd
dest_path=/etc/httpd/conf.d/

if grep -q Ubuntu /etc/*release ; then
    echo "Ubuntu detected"
    serv=apache2
    dest_path=/etc/apache2/sites-enabled/
fi
sudo cp *.crt /etc/pki/tls/certs/
sudo cp *.key /etc/pki/tls/private/
sudo cp *.conf $dest_path
sudo service $serv restart
