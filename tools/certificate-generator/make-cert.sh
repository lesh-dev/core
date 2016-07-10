#!/usr/bin/env bash

set -xe

function make_cert() {
    name="$1"
    if [ -r "$name.crt" ] && [ -r "$name.key" ] ; then
        echo "Certificate pair $name.crt + $name.key already exists, skipping"
        return 0
    fi
    openssl req -new -x509 -days 9999 -nodes -subj "/CN=$name/O=$name LLC/C=RU" -out $name.crt -keyout $name.key
}

make_cert "xclean.local"
make_cert "fizlesh.local"
make_cert "lesh.local"
make_cert "owncloud.lc"