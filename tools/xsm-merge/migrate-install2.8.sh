#!/usr/bin/env bash

set -e

mig_ver="2.8"

site_root="$1"
if [ -z "$site_root" ] ; then
    echo "Usage: $0 <site-root>"
    echo "Example: $0 /var/www/html/site"
    exit 1
fi


mig_root="$site_root/migrate$mig_ver"

mkdir -p "$mig_root"
cp *$mig_ver* "$mig_root/"
rm -f "$mig_root/migrate-install$mig_ver.sh"
