#!/usr/bin/env bash
set -e
set -x

DIR=$(dirname $0)
DBFILE="$1"

cat $DIR/schema.sql > /tmp/migration.sql
$DIR/dump-data.sh $DBFILE >> /tmp/migration.sql
cat $DIR/postprocessing.sql >> /tmp/migration.sql
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f /tmp/migration.sql

