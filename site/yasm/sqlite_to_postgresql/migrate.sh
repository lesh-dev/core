#!/usr/bin/env bash
set -e
set -x
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f ./schema.sql
./dump-data.sh ../fizlesh.sqlite3 > /tmp/sqlite-data.sql
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f /tmp/sqlite-data.sql

