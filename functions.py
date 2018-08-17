#!/usr/bin/python3
# pylint: disable=line-too-long
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  Copyright (c) 1995-2018, Ecometer s.n.c.
#  Author: Paolo Saudin.
#
#  Desc : Function collection
#  File : functions.py
#
#  Date : 17/08/2018 07:01:47
# ----------------------------------------------------------------------
""" Useful stuff
"""
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

if __name__ == '__main__':
    sys.exit(1)

def create_log(logging_level):
    """ Create log manager """
    # path
    logpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    # script name
    file_name = os.path.basename(sys.argv[0])
    # log name
    logname = os.path.join(logpath, file_name + '.log')

    # rotation once per day
    # https://docs.python.org/2/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
    handler = TimedRotatingFileHandler(logname,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    handler.suffix = "%Y%m%d" # %Y-%m-%d_%H-%M-%S
    logging.getLogger('').addHandler(handler)

    # formatter
    formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    # console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # formatter
    formatter_console = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')
    #formatter_console = logging.Formatter('%(message)s')
    console.setFormatter(formatter_console)
    logging.getLogger('').addHandler(console)

    # set custom level
    logging.getLogger('').setLevel(logging_level)
    console.setLevel(logging_level)

    # https://docs.python.org/3.4/library/logging.handlers.html?highlight=backupcount
    # CRITICAL 50
    # ERROR    40
    # WARNING  30
    # INFO     20
    # DEBUG    10
    # NOTSET    0

def clear_screen():
    """ Clear screen """
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('cls')

def unix_time(date_time):
    """ Get unit epoch time """
    epoch = datetime.utcfromtimestamp(0)
    delta = date_time - epoch
    return int(delta.total_seconds())

def unix_time_minutes(date_time):
    """ Get unit epoch time in minutes """
    return int(unix_time(date_time) / 60)
