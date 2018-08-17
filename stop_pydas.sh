#!/bin/bash
# Author : Paolo Saudin
# Description : stop python script
# Version 1

# --------- Info ---------
echo "stopping pydas script"

# --------- User Settings ---------
PROCESS2KILL="/home/pi/bin/pydas/pydas.py"

# --------- Run program ---------
echo "killing process id [`pgrep -f $PROCESS2KILL`]"
pkill -f "$PROCESS2KILL"

# --------- End ---------
echo "done"
