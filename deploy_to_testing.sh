#!/usr/bin/env bash

. deploy-tools/installer/installer.sh

$SHELL ./push_prod.sh
deploy_service fizlesh fizlesh.ru testing
