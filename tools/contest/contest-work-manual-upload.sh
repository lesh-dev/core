#!/usr/bin/env bash

works="/srv/www/clones/content-fizlesh.ru/content/contest/attach/contestants"

f="$1"
id="$2"
d=$( date '+%s' )
work_path="content/contest/attach/contestants/$d/$f"
echo $work_path
sudo sqlite3 "/srv/www/clones/content-fizlesh.ru/content/ank/fizlesh.sqlite3" <<EOF
    update contestants set work = '$work_path' where contestants_id = $id ;
EOF
sudo mkdir -p "$works/$d/"
sudo cp "$f" "$works/$d/"
sudo chown -R www-data:root "$works"
