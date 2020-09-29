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
#  Update : 2020-09-24 13:53
# ----------------------------------------------------------------------

# config
main = {
    # generic
    'polling_time' : 30,            # polling (seconds)
    'store_time' : 3600,            # store data (seconds)
    'data_path' : None,             # data path - set later on
    'ftp_path' : None,              # data path for ftp export - set later on
    'file_header' : 'xxxxxxxxxxxx', # data file header
    'ws_url' : 'https://xxxxxxxxxxxx/loggeralarms/0000/', # web service url
    'reset_alarm_msg_dealy' : 3600, # send a message to ackoledge no alarms (seconds)

    # specific for iono modules
    'use_ai' : False, # analog input
    'use_io' : True,  # digital io
    'use_ev' : True,  # digital io events
    'use_1w' : False, # one wire input (temperature)
    'use_ro' : False, # relay outputs
    'use_oc' : False, # open collectors
    'use_ld' : False, # on board led

    # override default configuration

    # digital input reverse
    'dr1' : None,
    'dr2' : None,
    'dr3' : None,
    'dr4' : None,
    'dr5' : None,
    'dr6' : None,
    # digital input name
    'dn1' : None, # contatto porta
    'dn2' : None, # contatto alimentazione
    'dn3' : None, # contatto temperatura alta
    'dn4' : None, # contatto flusso sonda
    'dn5' : None,
    'dn6' : None,

    # analog input name
    'an1' : None,
    'an2' : None,

    # one wire input name
    '1wn1' : None,

}
