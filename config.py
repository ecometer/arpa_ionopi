#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  Copyright (c) 1995-2020, Ecometer s.n.c.
#  Author: Paolo Saudin.
#
#  Desc : Configuration file for pydas
#  File : config.py
#
#  Date : 2020-02-07 07:56
#  Update :
# ----------------------------------------------------------------------

# config
main = {
    # generic
    'polling_time' : 30,            # polling (seconds)
    'store_time' : 3600,            # store data (seconds)
    'data_path' : None,             # data path - set later on
    'ftp_path' : None,              # data path for ftp export - set later on
    'file_header' : 'xxxxxxxxxxxx', # data file header
    'ws_url' : 'https://rmqa.arpal.gov.it/loggeralarms/0000/', # web service url
    'reset_alarm_msg_dealy' : 3600, # send a message to ackoledge no alarms (seconds)

    # specific for iono modules
    'use_ai' : False, # analog input
    'use_io' : True,  # digital io
    'use_ev' : True,  # digital io events
    'use_1w' : False, # one wire input (temperature)
    'use_ro' : False, # relay outputs
    'use_oc' : False, # open collectors
    'use_ld' : False, # on board led
}


#'http://rmqa.arpa.vda.it/loggeralarms/0000/'
#'http://192.168.0.12:8000/loggeralarms/0000/'
