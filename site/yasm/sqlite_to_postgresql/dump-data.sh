#!/usr/bin/env bash
set -e

filename="$1"

tables=$(echo .schema | sqlite3 "$filename" | grep -Eo 'CREATE TABLE( IF NOT EXISTS)? [^\(]+' | sed -e 's/CREATE TABLE//' -e 's/IF NOT EXISTS//')

# Но нам нужен определённый порядок
for tbl in school contestants problems solutions notification department course person course_teachers person_school exam submission xversion person_comment pss contact; do
    #echo "dumping $tbl" >&2
    (echo .mode insert; echo "SELECT * FROM $tbl;") | sqlite3 "$filename" | sed -e "s/INSERT INTO \"table\"/INSERT INTO public.$tbl/" -e "s/INSERT INTO table/INSERT INTO public.$tbl/"
done;
