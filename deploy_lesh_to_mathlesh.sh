#!/usr/bin/env bash

. deploy-tools/installer/installer.sh

$SHELL ./push_prod.sh
deploy_service lesh.org math-lesh.org production ""
