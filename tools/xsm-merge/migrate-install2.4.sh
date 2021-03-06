#!/usr/bin/env bash

set -e

site_root="$1"
if [ -z "$site_root" ] ; then
    echo "Usage: $0 <site-root>"
    echo "Example: $0 /var/www/html/site"
    exit 1
fi

mig_root="$site_root/migrate2.4"

mkdir -p "$mig_root"
cp *2.4* "$mig_root/"
rm -f "$mig_root/migrate-install2.4.sh"
