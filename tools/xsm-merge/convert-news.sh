#!/usr/bin/env bash
rm -rf ./new-news
mkdir -p ./new-news
php news-to-contlist.php news-list.txt
