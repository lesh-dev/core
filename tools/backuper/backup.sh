#!/usr/bin/env bash

set -xe

# VPS Backuper
# ------------
# Please DO NOT EDIT THIS FILE directly, these changes will be LOST
# when updating script from git repo.
# Instead, edit <git-repo-root>/tools/backuper/backup.sh and then deploy it
# to /srv/tools/backup.sh


# quota monitoring.
# backup may fail if no space is left, so let's begin with quotas.

backup_status_file=/tmp/backup-status
quota_status_file=/tmp/quota-status

my_dir="`dirname $0`"
quota_script="$my_dir/quota-monitor.py"

quota_settings="$my_dir/quota.txt"

if ! [ -r "$quota_settings" ]; then
    echo "Error: no quota settings '$quota_settings' found. "
    exit 1
fi

echo "Checking quotas. "

if ! $quota_script "$my_dir/quota.txt"; then
    echo "ERROR: Quota exceeded."
    echo "QUOTA_FAILED " > $quota_status_file
else
    echo "Quotas are OK. "
    echo "OK" > $quota_status_file
fi

# let's now backup.

echo "Performing backup. "

backup_folder=/backup

rm -rf "$backup_folder"
mkdir -p "$backup_folder"

backup_db()
{
    echo "Dumping database $1"
    db_encoding=utf8
    if ! [ -z "$3" ]; then
        db_encoding=$3
    fi
    mysqldump -ubackup -pnothing_to_backup --default-character-set=$db_encoding "$1" | gzip > "$2"
}

# add more folders here if you need
echo "Taring git..."
tar czf "$backup_folder/git.tgz"  /srv/git
echo "Taring trac..."
tar czf "$backup_folder/trac.tgz" /srv/trac
echo "Taring etc..."
tar czf "$backup_folder/etc.tgz"  /etc
backup_db smf "$backup_folder/forum.sql.gz"
backup_db postfix "$backup_folder/postfix.sql.gz" "latin1"

echo "Taring attachments..."
tar czf "$backup_folder/attach.tgz"  /srv/www/fizlesh.ru/forum/attachments

plan_a()
{
    echo "Performing backup plan A. "
    dest_host=doctor@doctor.dtdns.net
    rsync -avz "$backup_folder" "$dest_host:/data/backup/lesh/$back_date/"
}

plan_b()
{
    echo "Performing backup plan B. "
    dest_host=mvel@mvel.dtdns.net
    chown -R mvel:mvel $backup_folder
    dest_folder=backup/lesh/$back_date/
    ssh $dest_host mkdir -p $dest_folder
    # reverse scp-ying works!
    ssh $dest_host scp fizlesh.ru:$backup_folder/* $dest_folder
}

back_date="`date +%Y-%m-%d`"

if plan_a ; then
    echo "Backing to primary host $dest_host succeeded"
    echo "OK" > $backup_status_file
    exit 0
else
    echo "Backing to primary host $dest_host failed"
fi

if plan_b ; then
    echo "Backing to secondary host $dest_host succeeded"
    echo "OK" > $backup_status_file
    exit 0
else
    echo "Backing to secondary host $dest_host failed"
fi

# if we're here, backup failed.
echo "ERROR: Backup failed. "
echo "BACKUP_FAILED" > $backup_status_file
