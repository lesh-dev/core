#!/bin/bash -e
source $(dirname $0)/publish.conf
cat <<EOF
Production content checksum:     $CHECKSUM_CONTENT
Preproduction content checksum:  $CHECKSUM_NEXT
EOF

if [ "$CHECKSUM_CONTENT" != "$CHECKSUM_NEXT" ]; then
    cat <<EOF
Can't proceed. Content in preproduction is outdated.
   You may edited content during preproduction testing
   or someone edited main content.
   Now you can either:

    (u)  Update content in current preproduction
    (c)  Create new preproduction branch
    (e)  Do nothing (exit)

EOF
    while true; do
        read -p "Your choice? (u/c/e): " answer
        if [ $answer. == 'u.' ]; then
            echo "publish.update script will be executed. You've to run $0 again."
            publish.update
            exit 1
        fi
        if [ $answer. == 'c.' ]; then
            echo "publish.preprod script will be executed. You've to run $0 again."
            publish.preprod
            exit 1
        fi
        if [ $answer. == 'e.' ]; then
            exit 1
        fi
    done
    exit 1
fi

cat <<EOF
You're about to make a new prodution copy from preproduction.
Type 'yes' if you're understanding what you're doing and want to proceed.
EOF
read -p "Type 'yes' if you're sure that preproduction branch works (yes/no): " answer
if [ "$answer." != "yes." ]; then
    echo "Cancelled by user"
    exit 1
fi

export FINAL=$CLONE_DIR/production
export LAST=$CLONE_DIR/production.last
export NEWPROD=$CLONE_DIR/production.$TIMESTAMP
touch $FINAL
touch $LAST
if [ -d $NEWPROD ]; then
    echo "$NEWPROD already exists!"
    exit 1
fi

if [ -f $PREPROD/install.php ]; then
    echo "your 'production' branch contains install.php! Please, think before you type!"
    exit 1
fi

cp -rf $(readlink $PREPROD) $NEWPROD
chown -R www-data $NEWPROD
rm -rf $NEWPROD/.prec/*
rm -rf $NEWPROD/content
ln -s $CONTENT $NEWPROD/content

cat > $NEWPROD/INFO <<EOF
<b><font color="green">production</font></b>
$BRANCH
$TIMESTAMP
EOF

rm $LAST
ln -s $NEWPROD $LAST
apachectl -k graceful

cat <<EOF
=====================================================
              LAST CHANCE TO QUIT!!!
=====================================================
Now, take a brief look to website:

      http://last-chance.lesh-dev.dtdns.net

This is EXACT copy of site you're going to make
a PRODUCTION copy.
BE CAREFUL: If you edit content at last-chance site,
changes will be immediately commited to main
(production) site.
EOF

while true; do
    read -p "Are you sure that EVERYTHING IS OK? Press Y to continue (y/n)" answer
    if [ $answer. == 'y.' ]; then
        rm $FINAL
        ln -s $NEWPROD $FINAL
        apachectl -k graceful
        echo "Production copy created."
        exit 0
    elif [ $answer. == 'n.' ]; then
        echo "Cancelled by user. Production site is untouched"
        exit 1
    fi
done
