#!/bin/bash
# Author : Paolo Saudin
# Description : purge old files
# Version 1

echo "analizzo $HOME/bin/pydas/log/*.log"
find $HOME/bin/pydas/log/ -name '*.log' -mtime +120 -type f -exec rm -vr {} \;
#find $HOME/bin/pydas/log/ -name '*.log' -mtime +120 -type f -exec echo {} \;

echo "analizzo $HOME/bin/pydas/data/*.dat"
find $HOME/bin/pydas/data/ -name '*.dat' -mtime +120 -type f -exec rm -vr {} \;
#find $HOME/bin/pydas/data/ -name '*.dat' -mtime +120 -type f -exec echo {} \;

echo "analizzo $HOME/bin/pydas/ftp_back/*.dat"
find $HOME/bin/pydas/ftp_back/ -name '*.dat' -mtime +120 -type f -exec rm -vr {} \;
#find $HOME/bin/pydas/ftp_back/ -name '*.dat' -mtime +120 -type f -exec echo {} \;
