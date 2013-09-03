#!/usr/bin/env bash

mig_root="/var/www/html/site/migrate2.4"

sudo mkdir -p "$mig_root"
sudo cp *2.4* "$mig_root/"
sudo rm -f "$mig_root/migrate-install2.4.sh"