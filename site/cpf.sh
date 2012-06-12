#!/bin/bash

for f in `cat ifiles`; do
    echo $f
    dn="`dirname $f`"
    nf="$dn/newinf"
    cp /var/www/html/site/$dn/newinf $dn/info
done
