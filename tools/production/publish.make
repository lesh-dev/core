#!/bin/bash -e
source $(dirname $0)/publish.conf
echo Production content checksum:     $CHECKSUM_CONTENT
echo Preproduction content checksum:  $CHECKSUM_NEXT
if [ "$CHECKSUM_CONTENT" != "$CHECKSUM_NEXT" ]; then
 echo "Can't proceed. Content in preproduction is outdated. "
 echo "  You may edited content during preproduction testing or someone edited main content "
 echo "  Now you can:"
 echo "   (u). Update content in current preproduction"
 echo "   (c). Create new preproduction branch"
 echo "   (e). Do nothing"
 while [ true ]; do
   read -p "Your choise? (u/c/e): " answer
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
echo "You're about to make a new prodution copy from preproduction."
echo " Type 'yes' if you're understanding what You're doing and want to proceed. "
read -p "Type 'yes' if You're sure that preproduction branch works (yes/no): " answer
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

echo "<b><font color='green'>production</font></b>" > $NEWPROD/INFO
echo "$BRANCH" >> $NEWPROD/INFO
echo "$TIMESTAMP" >> $NEWPROD/INFO


rm $LAST
ln -s $NEWPROD $LAST
apachectl -k graceful

echo "====================================================="
echo "              LAST CHANCE TO QUIT!!!"
echo "====================================================="
echo "Now, take a brief look to website: "
echo ""
echo "      http://last-chance.lesh-dev.dtdns.net"
echo ""
echo "This is EXACT copy of site You're going to make production copy."
echo "BE CAREFUL: if You edit content at last-chance site, "
echo "changes will be immidiately commited to main (production) site, so -- be aware"
echo ""
while [ true ]; do
  read -p "ARE YOU SURE, THAT ALL IS OK AND WANT TO CONTINUE? (y/n)" answer
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
