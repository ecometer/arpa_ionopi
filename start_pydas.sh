#!/bin/bash
# Author : Paolo Saudin
# Description : run python script at startup
# Version 1

# --------- Info ---------
echo "running smartdas script"

# --------- User Settings ---------
PROCESS2RUN="/home/pi/bin/pydas/pydas.py"

# --------- Run program ---------
/usr/bin/python3 $PROCESS2RUN 2>&1 /home/pi/bin/pydas/log/start_pydas.log &
VAR=`pgrep -f "$PROCESS2RUN"`
echo "program pid $VAR"

# ---------------------------------
echo "done"
