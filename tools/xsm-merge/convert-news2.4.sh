#!/usr/bin/env bash

set -xe

(cd news && ls -1 *.news > ../news-list.txt && cd .. )
rm -rf ./new-news
mkdir -p ./new-news
cp news/template new-news/
php ./news-to-contlist.php ./news-list.txt
