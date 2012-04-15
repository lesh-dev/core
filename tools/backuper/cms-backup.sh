#!/bin/bash
LOG="fizlesh.ru-backup.log"
echo "== `date +%Y.%m.%d-%H:%M:%S`: Backup process started  ==" >> $LOG
#rm -rf ./fizlesh.ru
# -X /data/cms/pages/z01News,/data/cms/pages/z065Photoalbum
WGET_PARAMS="--timestamping --user=dmvn@speleoastronomy.org --password=cCkYAxtHdU5g -r --no-parent --no-verbose"

wget $WGET_PARAMS ftp://fizlesh.ru/data/cms/pages/ -o pages.log
cat pages.log >> $LOG
echo "   `date +%Y.%m.%d-%H:%M:%S`: Content download complete" >> $LOG
wget $WGET_PARAMS ftp://fizlesh.ru/ank -o ank.log
cat ank.log >> $LOG
echo "   `date +%Y.%m.%d-%H:%M:%S`: Anketas download complete" >> $LOG
wget $WGET_PARAMS ftp://fizlesh.ru/data/auth/usr -o usr.log
cat usr.log >> $LOG
echo "   `date +%Y.%m.%d-%H:%M:%S`: Usr dir download complete" >> $LOG
rm -f pages.log ank.log usr.log
echo "   `date +%Y.%m.%d-%H:%M:%S`: Removed temporary wget logs" >> $LOG
hg add
hg commit -m "daily backup" -u autobackuper
echo "   `date +%Y.%m.%d-%H:%M:%S`: Commited to repo" >> $LOG

echo "== `date +%Y.%m.%d-%H:%M:%S`: Backup process finished ==" >> $LOG
#hg push

                                                                                     