#!/bin/bash
# Author : Paolo Saudin
# Description : send data files to ftp server
# Version 1

# sudo apt install ncftp

# lock dir/file
BASEDIR=$(dirname $0)
SCRIPTFILE=$(basename $0)
LOCKFILE="${BASEDIR}/${SCRIPTFILE}.pid"
echo $LOCKFILE

echo
echo "Running script -> $SCRIPTFILE @ `date`"
echo "Lockfile -> $LOCKFILE"

# script already running check
if [ -e $LOCKFILE ] && kill -0 `cat $LOCKFILE`
then
    echo "$SCRIPTFILE already running. Aborting."
    exit
fi
trap "rm -fv $LOCKFILE; exit" INT TERM EXIT
echo $$ > $LOCKFILE

#
# main script
#

# ftp
FTP_HOST='ftp.arpal.gov.it'
FTP_USER='Inventarioemissioni'
FTP_PASS='Pwf43.4.4$$fRat'
FTP_PATH='/dati_iono'

# local
LOCAL_PATH='/home/pi/bin/pydas/ftp/'
LOCAL_FILES='/home/pi/bin/pydas/ftp/*.dat'
LOCAL_PATH_BACK='/home/pi/bin/pydas/ftp_back'
# mkdir -p /home/pi/bin/pydas/ftp_back

echo "Checking for data files [dat]"
COUNT=`ls -1 $LOCAL_FILES 2>/dev/null | wc -l`
if [ $COUNT == 0 ]; then
    echo "No data files found!"
    exit 0
fi

echo "Ftpiing data"
OUT=$(ncftpput -v -u $FTP_USER -p $FTP_PASS $FTP_HOST $FTP_PATH $LOCAL_FILES 2>&1)
# check exit code
if [ $? -ne 0 ]; then
    echo "Error: $OUT"
    exit 1
else
    echo "Result: $OUT"
fi

echo "Moving file from $LOCAL_PATH to $LOCAL_PATH_BACK"
OUT=$(mv -v "$LOCAL_PATH/"* "$LOCAL_PATH_BACK/" 2>&1)
# check exit code
if [ $? -ne 0 ]; then
    echo "Error: $OUT"
    exit 1
else
    echo "Result: $OUT"
fi

echo "Done"

# Terminate our shell script with success message
exit 0 
