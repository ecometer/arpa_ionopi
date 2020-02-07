#!/usr/bin/python3
# pylint: disable=broad-except, line-too-long
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  Copyright (c) 1995-2018, Ecometer s.n.c.
#  Author: Paolo Saudin.
#
#  Desc : Sferalabs Iono Pi
#  File : iono.py
#
#  Date : 14/08/2018 08:56:28
# ----------------------------------------------------------------------
""" Sfera Labs S.r.l. IonoPI Python Class

    # custom function for subclass to override
    parse_event(self, din)
"""
import sys
import os
import glob
import logging
import logging.config
import spidev
import RPi.GPIO as GPIO
import iono_config

if __name__ == '__main__':
    sys.exit(1)

class Iono:
    """ Iono main class """

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
        {'gpio': TTL1, 'id': 1, 'dbid': one_wire_inputs[0]['dbid'], 'code': None, 'name': 'WI 1', 'value': None},
    ]

    digital_inputs = [ # Generic digital input
        {'gpio': DI1, 'id': 1, 'dbid': digital_inputs[0]['dbid'], 'name': 'DI 1', 'reverse' : digital_inputs[0]['reverse'], 'status': 0, 'status_ev': 0},
        {'gpio': DI2, 'id': 2, 'dbid': digital_inputs[1]['dbid'], 'name': 'DI 2', 'reverse' : digital_inputs[1]['reverse'], 'status': 0, 'status_ev': 0},
        {'gpio': DI3, 'id': 3, 'dbid': digital_inputs[2]['dbid'], 'name': 'DI 3', 'reverse' : digital_inputs[2]['reverse'], 'status': 0, 'status_ev': 0},
        {'gpio': DI4, 'id': 4, 'dbid': digital_inputs[3]['dbid'], 'name': 'DI 4', 'reverse' : digital_inputs[3]['reverse'], 'status': 0, 'status_ev': 0},
        {'gpio': DI5, 'id': 5, 'dbid': digital_inputs[4]['dbid'], 'name': 'DI 5', 'reverse' : digital_inputs[4]['reverse'], 'status': 0, 'status_ev': 0},
        {'gpio': DI6, 'id': 6, 'dbid': digital_inputs[5]['dbid'], 'name': 'DI 6', 'reverse' : digital_inputs[5]['reverse'], 'status': 0, 'status_ev': 0},
    ]

    analog_inputs = [ # Analog input (on terminal block) to A/D
        {'ch': AI1, 'id': 1, 'dbid': analog_inputs[0]['dbid'], 'name': 'AI 1', 'value': None},
        {'ch': AI2, 'id': 2, 'dbid': analog_inputs[0]['dbid'], 'name': 'AI 2', 'value': None},
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

    def __init__(self, config):
        """ Constructor """
        logging.getLogger('')
        logging.debug("Function __init__")

        # Set channel mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # set properties
        self.config = config

        # Main spi object
        self.spi = None

        # Set analog input
        if self.config['use_ai']:
            self._set_analog_inputs()

        # Set digital io
        if self.config['use_io']:
            self._set_digital_io()
        # Enable events
        if self.config['use_ev']:
            self._set_digital_io_events()

        # One wire path and auto detection (first one)
        if self.config['use_1w']:
            if self.one_wire_inputs[0]['code'] is None:
                self._find_1wire_ds18b20()

        # Set relay outputs
        if self.config['use_ro']:
            self._set_relay_outputs()

        # Set open collectors
        if self.config['use_oc']:
            self._set_collectors_outputs()

        # Set on board led
        if self.config['use_ld']:
            self._set_onboard_led()

    def cleanup(self):
        """  Cleanup  """
        logging.debug("Function _cleanup")

        try:
            GPIO.cleanup()
            if self.spi:
                self.spi.close()
        except Exception:
            pass

    def _set_analog_inputs(self):
        """ Setup analog input """
        logging.debug("Function _set_analog_inputs")

        try:
            # Initialize spi
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 50000
            self.spi.mode = 0b01

        except Exception as ex:
            logging.critical("An exception was encountered in _set_analog_inputs: %s", str(ex))

    def _set_digital_io(self):
        """ Setup digital input/output """
        logging.debug("Function _set_digital_io")
        # https://sourceforge.net/p/raspberry-channel-python/wiki/Inputs/
        try:
            logging.debug("Setting GPIO mode PUD_DOWN")
            # Pull_up_down=GPIO.PUD_UP | PUD_DOWN
            # PUD_DOWN set to 0 until 3v3 is applied to pin
            GPIO.setup(self.DI1, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.DI2, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.DI3, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.DI4, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.DI5, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.DI6, GPIO.IN) # , pull_up_down=GPIO.PUD_DOWN)

        except Exception as ex:
            logging.critical("An exception was encountered in _set_digital_io: %s", str(ex))

    def _set_digital_io_events(self):
        """ Start digital IO polling with callback """
        logging.debug("Function _set_digital_io_events")

        try:

            # GPIO.FALLING | GPIO.RISING | GPIO.BOTH
            GPIO.add_event_detect(self.DI1, GPIO.RISING, callback=self._io_callback, bouncetime=500)
            GPIO.add_event_detect(self.DI2, GPIO.RISING, callback=self._io_callback, bouncetime=500)
            GPIO.add_event_detect(self.DI3, GPIO.RISING, callback=self._io_callback, bouncetime=500)
            GPIO.add_event_detect(self.DI4, GPIO.RISING, callback=self._io_callback, bouncetime=500)
            GPIO.add_event_detect(self.DI5, GPIO.RISING, callback=self._io_callback, bouncetime=500)
            GPIO.add_event_detect(self.DI6, GPIO.RISING, callback=self._io_callback, bouncetime=500)

        except Exception as ex:
            logging.critical("An exception was encountered in _set_digital_io_events: %s", str(ex))

    def _set_relay_outputs(self):
        """ Setup digital input/output """
        logging.debug("Function _set_relay_outputs")

        # https://sourceforge.net/p/raspberry-channel-python/wiki/Inputs/
        try:
            logging.debug("Setting GPIO mode OUT")
            GPIO.setup(self.OR1, GPIO.OUT)
            GPIO.setup(self.OR2, GPIO.OUT)
            GPIO.setup(self.OR3, GPIO.OUT)
            GPIO.setup(self.OR4, GPIO.OUT)

        except Exception as ex:
            logging.critical("An exception was encountered in _set_relay_outputs: %s", str(ex))

    def _set_collectors_outputs(self):
        """ Setup digital input/output """
        logging.debug("Function _set_collectors_outputs")

        # https://sourceforge.net/p/raspberry-channel-python/wiki/Inputs/
        try:
            logging.debug("Setting GPIO mode OUT")
            GPIO.setup(self.OC1, GPIO.OUT)
            GPIO.setup(self.OC1, GPIO.OUT)
            GPIO.setup(self.OC1, GPIO.OUT)

        except Exception as ex:
            logging.critical("An exception was encountered in _set_collectors_outputs: %s", str(ex))

    def _set_onboard_led(self):
        """ Setup on board led """
        logging.debug("Function _set_onboard_led")

        try:
            # Set a port/pin as an output
            GPIO.setup(self.L1, GPIO.OUT)
            # Switch led off
            self.set_led_status(False)

        except Exception as ex:
            logging.critical("An exception was encountered in _set_onboard_led: %s", str(ex))

    def _io_callback(self, channel):
        """ Callback event """
        logging.debug("Function _io_callback - GPIO %s", channel)

        # Find digital input by gpio channel
        din = next((item for item in self.digital_inputs if item["gpio"] == channel), None)

        # Get status (on/off)
        status = GPIO.input(channel)
        logging.debug("Status %s", status)
        if din['reverse']:
            status = int(not status)
            logging.debug("Reversed status %s", status)

        # If status is zero we skip away - if not status:
        if din['status_ev'] == status:
            return

        # Set new status
        din['status_ev'] = status

        # custom function for subclass to override
        self.parse_event(din)

    def _get_analog_value(self, channel):
        """ Read analog value from AIx """
        logging.debug("Function _get_analog_value - Channel %s", channel)

        # The Iono Pi library uses a 0.007319 conversion factor
        # for the AI1 and AI2 inputs with a
        # 0÷30V range, and 0.000725 for AI3 and AI4 inputs with a 0÷3V range
        adc = self.spi.xfer2([6, channel<<6, 0])
        data = ((adc[1] & 15) << 8) + adc[2]

        factor = 0.007319
        value = data * factor
        logging.debug("Value: %s", value)
        return value

    def _find_1wire_ds18b20(self):
        """ Find first DS18B20 """
        logging.debug("Function _find_1wire_ds18b20")

        try:
            # Get device paths
            logging.debug("Glob: %s", self.one_wire_base_dir + '28*')
            device_folders = glob.glob(self.one_wire_base_dir + '28*')
            if len(device_folders) >= 1:
                device_folder = device_folders[0]
                #logging.debug("Device folder: %s", device_folder)
                # ['/sys/bus/w1/devices/28-0000075e0152']
                basename = os.path.basename(device_folder)
                logging.debug("Basename: %s", basename)
                self.one_wire_inputs[0]['code'] = str(basename)
            else:
                logging.warning("No devices found")

        except Exception as ex:
            logging.error("An exception was encountered in _find_1wire_ds18b20() : %s", str(ex))

    def _get_1wire_raw_data(self, sens_id):
        """ Read the temperature message from the device file """
        logging.debug("Function _get_1wire_raw_data")

        try:
            # Build device filename
            device_file = self.one_wire_base_dir + '/' + sens_id + '/w1_slave'
            if not os.path.exists(device_file):
                logging.error("Sensor directory does not exists: %s", device_file)
                return None

            file = open(device_file, 'r')
            lines = file.readlines()
            file.close()
            return lines

        except Exception as ex:
            logging.error("An exception was encountered in _get_1wire_raw_data() : %s", str(ex))
            return None

    def _read_temp(self, sens_id):
        """ Split the actual temperature out of the message """
        logging.debug("Function _read_temp() - Id %s", sens_id)

        try:

            # If no sensor return
            if sens_id is None:
                return float('nan')

            # Get file content
            lines = self._get_1wire_raw_data(sens_id)
            if lines is None:
                return float('nan')

            if lines[0].strip()[-3:] != 'YES':
                return float('nan')

            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return temp_c

            return float('nan')

        except Exception as ex:
            logging.error("An exception was encountered in _read_temp() : %s", str(ex))
            return float('nan')

    # Setters

    def set_relay_status(self, channel, status):
        """ Set on board led status on/off """
        logging.debug("Function set_relay_status")

        try:
            # Get output
            rel = next((item for item in self.relay_outputs if item["id"] == channel), None)
            # Set status
            rel['status'] = status
            logging.debug("GPIO %s, id %s, status %s",
                          rel['name'], rel['id'], rel['status'])

            # Set port/pin value to 1/GPIO.HIGH/True
            if channel == 1:
                GPIO.output(self.OR1, status)
            elif channel == 2:
                GPIO.output(self.OR2, status)
            elif channel == 3:
                GPIO.output(self.OR3, status)
            elif channel == 4:
                GPIO.output(self.OR4, status)

        except Exception as ex:
            logging.critical("An exception was encountered in set_relay_status: %s", str(ex))

    def set_open_collector_status(self, channel, status):
        """ Set on board led status on/off """
        logging.debug("Function set_open_collector_status")

        try:
            # Get output
            opc = next((item for item in self.open_collector_outputs if item["id"] == channel), None)

            # Set status
            opc['status'] = status
            logging.debug("GPIO %s, id %s, status %s",
                          opc['name'], opc['id'], opc['status'])

            # Set port/pin value to 1/GPIO.HIGH/True
            if channel == 1:
                GPIO.output(self.OC1, status)
            elif channel == 2:
                GPIO.output(self.OC2, status)
            elif channel == 3:
                GPIO.output(self.OC3, status)

        except Exception as ex:
            logging.critical("An exception was encountered in set_open_collector_status: %s", str(ex))

    def set_led_status(self, status):
        """ Set on board led status on/off """
        logging.debug("Function set_led_status")

        try:
            # Get status text
            sttext = 'on' if status else 'off'
            logging.debug("Setting led to %s", sttext)
            # Set port/pin value to 1/GPIO.HIGH/True
            GPIO.output(self.L1, status)

        except Exception as ex:
            logging.critical("An exception was encountered in set_led_status: %s", str(ex))

    # def reset_digital_input_events(self):
    #     """ Reset digital input events array """
    #     logging.info("Function reset_digital_input_events")

    #     try:
    #         # Reset digital_inputs
    #         logging.debug("Resetting digital inputs")
    #         for din in self.digital_inputs:
    #             din['status_ev'] = 0

    #     except Exception as ex:
    #         logging.critical("An exception was encountered in reset_digital_input_events: %s", str(ex))

    # Getters

    def get_digital_input(self):
        """ Show all digital_inputs status """
        logging.debug("Function get_digital_input")

        try:
            # Loop through digital_inputs
            logging.debug("Looping through digital inputs")

            # Loop
            for din in self.digital_inputs:

                # Get status (on/off)
                status = GPIO.input(din['gpio'])
                logging.debug("Status %s", status)
                if din['reverse']:
                    status = int(not status)
                    logging.debug("Reversed status %s", status)

                din['status'] = status
                logging.debug("GPIO %s, id %s, status %s",
                              din['name'], din['id'], din['status'])

        except Exception as ex:
            logging.critical("An exception was encountered in get_digital_input: %s", str(ex))

    def get_analog_input(self):
        """ Show all analog inputs """
        logging.debug("Function get_analog_input")

        try:
            # Loop through items
            logging.debug("Looping through analog inputs")
            for ain in self.analog_inputs:
                ain['value'] = self._get_analog_value(ain['id'])
                logging.debug("Measure %s, id %s, value %s",
                              ain['name'], ain['id'], ain['value'])

        except Exception as ex:
            logging.critical("An exception was encountered in get_analog_input: %s", str(ex))

    def get_one_wire_input(self):
        """ Get ambience temperature """
        logging.debug("Function get_one_wire_input")

        try:
            # Loop through 1 wire input
            logging.debug("Looping through 1 wire input")
            for owi in self.one_wire_inputs:
                owi['value'] = self._read_temp(owi['code'])
                logging.debug("Measure %s, code %s, value %s",
                              owi['name'], owi['code'], owi['value'])

        except Exception as ex:
            logging.critical("An exception was encountered in get_one_wire_input: %s", str(ex))

    def get_relay_output(self):
        """ Show all relay outputs """
        logging.debug("Function get_relay_output")

        try:
            # Loop through relay outputs
            logging.debug("Looping through relay outputs")

            # Loop
            for rel in self.relay_outputs:

                # Get status (on/off)
                logging.debug("GPIO %s, id %s, status %s",
                              rel['name'], rel['id'], rel['status'])

        except Exception as ex:
            logging.critical("An exception was encountered in get_relay_output: %s", str(ex))

    def get_open_collector_output(self):
        """ Show all open collector outputs """
        logging.debug("Function get_open_collector_output")

        try:
            # Loop through relay outputs
            logging.debug("Looping through open collector outputs")

            # Loop
            for opc in self.open_collector_outputs:

                # Get status (on/off)
                logging.debug("GPIO %s, id %s, status %s",
                              opc['name'], opc['id'], opc['status'])

        except Exception as ex:
            logging.critical("An exception was encountered in get_open_collector_output: %s", str(ex))

    def parse_event(self, din):
        """ Parse event """
        # custom function for subclass to override
        # do something with the event, log, send telegram, ecc
        pass
