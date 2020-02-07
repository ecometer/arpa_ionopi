#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  Copyright (c) 1995-2020, Ecometer s.n.c.
#  Author: Paolo Saudin.
#
#  Desc : Configuration file for iono module
#  File : iono-config.py
#
#  Date : 2020-02-07 07:52
#  Update :
# ----------------------------------------------------------------------

L1 = 7    # GPIO7 out On-board green LED
OR1 = 17  # GPIO17 out Power relay 1
OR2 = 27  # GPIO27 out Power relay 2
OR3 = 22  # GPIO22 out Power relay 3
OR4 = 23  # GPIO23 out Power relay 4
AI1 = 1   # in Analog input 1 (on terminal block) to A/D   - 0b01000000 // MCP_CH1
AI2 = 2   # in Analog input 2 (on terminal block) to A/D   - 0b00000000 // MCP_CH0
AI3 = 3   # in Analog input 3 (on board pin header) to A/D - 0b10000000 // MCP_CH2
AI4 = 4   # in Analog input 4 (on board pin header) to A/D - 0b11000000 // MCP_CH3
TTL1 = 4  # GPIO4 in/out 1-Wire, Wiegand or generic TTL I/O
TTL2 = 26 # GPIO26 in/out 1-Wire, Wiegand or generic TTL I/O
TTL3 = 20 # GPIO20 in/out 1-Wire, Wiegand or generic TTL I/O
TTL4 = 21 # GPIO21 in/out 1-Wire, Wiegand or generic TTL I/O
DI1 = 16  # GPIO16 in generic digital input 1
DI2 = 19  # GPIO19 in generic digital input 2
DI3 = 13  # GPIO13 in generic digital input 3
DI4 = 12  # GPIO12 in generic digital input 4
DI5 = 6   # GPIO6 in generic digital input 5
DI6 = 5   # GPIO5 in generic digital input 6
OC1 = 18  # GPIO18 out open collector output 1
OC2 = 25  # GPIO25 out open collector output 2
OC3 = 24  # GPIO24 out open collector output 3


one_wire_base_dir = '/sys/bus/w1/devices/' # 1-Wire base path
one_wire_inputs = [ # 1-Wire, Wiegand or generic TTL I/O GPIO4
    {'gpio': TTL1, 'id': 1, 'dbid': None, 'code': None, 'name': 'WI 1', 'value': None},
]

digital_inputs = [ # Generic digital input
    {'gpio': DI1, 'id': 1, 'dbid': None, 'name': 'DI 1', 'reverse' : None, 'status': 0, 'status_ev': 0},
    {'gpio': DI2, 'id': 2, 'dbid': None, 'name': 'DI 2', 'reverse' : None, 'status': 0, 'status_ev': 0},
    {'gpio': DI3, 'id': 3, 'dbid': None, 'name': 'DI 3', 'reverse' : None, 'status': 0, 'status_ev': 0},
    {'gpio': DI4, 'id': 4, 'dbid': None, 'name': 'DI 4', 'reverse' : None, 'status': 0, 'status_ev': 0},
    {'gpio': DI5, 'id': 5, 'dbid': None, 'name': 'DI 5', 'reverse' : None, 'status': 0, 'status_ev': 0},
    {'gpio': DI6, 'id': 6, 'dbid': None, 'name': 'DI 6', 'reverse' : None, 'status': 0, 'status_ev': 0},
]

analog_inputs = [ # Analog input (on terminal block) to A/D
    {'ch': AI1, 'id': 1, 'dbid': None, 'name': 'AI 1', 'value': None},
    {'ch': AI2, 'id': 2, 'dbid': None, 'name': 'AI 2', 'value': None},
]

relay_outputs = [ # Power relay
    {'gpio': OR1, 'id': 1, 'name': 'OR 1', 'status': 0,},
    {'gpio': OR2, 'id': 2, 'name': 'OR 2', 'status': 0,},
    {'gpio': OR3, 'id': 3, 'name': 'OR 3', 'status': 0,},
    {'gpio': OR4, 'id': 4, 'name': 'OR 4', 'status': 0,},
]

open_collector_outputs = [ # Open collector output
    {'gpio': OC1, 'id': 1, 'name': 'OC 1', 'status': 0,},
    {'gpio': OC2, 'id': 2, 'name': 'OC 2', 'status': 0,},
    {'gpio': OC3, 'id': 3, 'name': 'OC 3', 'status': 0,},
]

onboard_led = [ # On-board green LED
    {'ch': L1, 'id': 1, 'name': 'LED 1', 'status': 0},
]
