#!/bin/bash -e

# VPS Backuper
# ------------
# Please DO NOT EDIT THIS FILE directly, these changes will be LOST
# when updating script from git repo.
# Instead, edit <git-repo-root>/tools/backuper/backup.sh and then deploy it
# to /srv/tools/backup.sh

backup_folder=/backup
status_file=/tmp/backup-status

rm -rf $backup_folder
mkdir -p $backup_folder

# add more folders here if you need
tar cvzf $backup_folder/git.tgz  /srv/git
tar cvzf $backup_folder/trac.tgz /srv/trac
tar cvzf $backup_folder/etc.tgz  /etc

plan_a()
{
    rsync -avz $backup_folder $dest_host:/data/backup/lesh/$back_date/
}

plan_b()
{
    dest_host=doctor@doctor.dtdns.net
    chown -R mvel:mvel $backup_folder
    # reverse scp-ying works!
    dest_host=mvel@mvel.dtdns.net
    dest_folder=backup/lesh/$back_date/
    ssh $dest_host mkdir -p $dest_folder
    # reverse scp-ying works!
    ssh $dest_host scp fizlesh.ru:$backup_folder/* $dest_folder
}

back_date="`date +%Y-%m-%d`"

if plan_a ; then
    echo "Backing to primary host $dest_host succeeded" 1>&2
    echo "OK" > $status_file
    exit 0
else
    echo "Backing to primary host $dest_host failed" 1>&2
fi

if plan_b ; then
    echo "Backing to secondary host $dest_host succeeded" 1>&2
    echo "OK" > $status_file
    exit 0
else
    echo "Backing to secondary host $dest_host failed" 1>&2
fi
