#!/bin/bash
LOG="fizlesh.ru-backup.log"
echo "== `date`:Backup process started  ==" >> $LOG
rm -rf ./fizlesh.ru
wget --user="dmvn@speleoastronomy.org" --password="cCkYAxtHdU5g" -q -r -np -R '*.jpeg,*.jpg,*.html' -X /data/cms/pages/z01News,/data/cms/pages/z065Photoalbum ftp://fizlesh.ru/data/cms/pages/z025AboutUs 
echo "   `date`:Content download complete" >> $LOG
wget --user="dmvn@speleoastronomy.org" --password="cCkYAxtHdU5g" -q -r -np -R '*.jpeg,*.jpg,*.html' ftp://fizlesh.ru/ank
echo "   `date`:Anketas download complete" >> $LOG
wget --user="dmvn@speleoastronomy.org" --password="cCkYAxtHdU5g" -q -r -np -R '*.jpeg,*.jpg,*.html' ftp://fizlesh.ru/data/auth/usr
echo "   `date`:Usr dir download complete" >> $LOG
hg add
hg commit -m "daily backup" -u autobackuper
echo "   `date`:Commited to repo" >> $LOG
echo "== `date`:Backup process finished ==" >> $LOG
#hg push

