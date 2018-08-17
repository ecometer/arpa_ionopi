#!/usr/bin/python3
# pylint: disable=broad-except, line-too-long
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
#  Copyright (c) 1995-2018, Ecometer s.n.c.
#  Author: Paolo Saudin.
#
#  Desc : Sferalabs Iono Pi Custom Class
#  File : iono.py
#
#  Date : 15/08/2018 07:53:24
# ----------------------------------------------------------------------
""" Arpa Vda Custom Class
"""
import sys
import os
import logging
import logging.config
from datetime import datetime
import threading
from math import sqrt
import requests
from iono import Iono

if __name__ == '__main__':
    sys.exit(1)

class IonoArpaVda(Iono):
    """ Arpa iono main class """
    def __init__(self, config, config_iono):
        super().__init__(config_iono)

        # set properties
        self.config = config

        # temperature stuff
        self.decimals = 2
        self.data_temperature = []
        #self.one_wire_inputs[0]['db_id'] = 1 # set database id
        self.analog_inputs[0]['db_id'] = 1 # set database id

        # alarm and messages flag
        self.alarm_cur = 0 # current alarm
        self.alarm_old = 0
        self.alarm_counter = 0
        self.alarm_sent = False
        self.alarm_door_sent = False
        self.alarm_send_reset_delay = config['reset_alarm_msg_dealy']

    def _mean(self, lst):
        """ Calculate mean """
        logging.debug("Calculating mean")
        if not lst:
            return float(None)

        return float(sum(lst)) / len(lst)

    def _stddev(self, lst):
        """ Calculate standard deviation """
        logging.debug("Calculating standard deviation")
        data_mean = self._mean(lst)
        data_sum = 0

        for item in lst:
            data_sum += pow(item - data_mean, 2)

        return sqrt(float(data_sum) / (len(lst) - 1))

    def _send_alarm(self):
        """ Send alarm to web server """
        logging.info("Function _send_alarm")
        try:

            # dump data to file
            logging.info("Sending alarm to web server [%s]", str(self.alarm_cur))

            # build file_name
            logging.debug("Store alarm")
            now = datetime.now()
            file_name = os.path.join(
                self.config['data_path'],
                self.config['file_header']+"_"+now.strftime('%Y-%m-%d')+".alarm"
            )
            # header
            row = now.strftime('%Y-%m-%d %H:%M:%S.%f') # datetime
            row += "\t"
            row += str(self.alarm_cur) # self.alarm_cur
            row += "\n"
            # dump data to file
            with open(file_name, "a") as file:
                file.write(row)

            # make HTTP request
            url = self.config['ws_url'] + str(self.alarm_cur)
            logging.debug("Url: %s ", url)
            req = requests.get(url)
            logging.debug("Result: %s ", req.status_code)
            # -> req.headers['content-type']
            # -> req.encoding
            # -> req.text
            # -> req.raw
            # -> req.json()

        except Exception as ex:
            logging.error("An exception was encountered in _send_alarm: %s", str(ex))

    def append_temperature(self):
        """ Store new data into array """
        logging.debug("Function append_temperature")

        # get item
        ain = self.analog_inputs[0]
        if ain and ain['value']:
            # calculate temp in °C - 0÷10 Vdc 0÷50°C
            temp = float(ain['value']) * 5
            logging.debug("Appending %s to temperature list", temp)
            # append data
            self.data_temperature.append(temp)
            logging.debug(self.data_temperature)

        # get item
        # owi = self.one_wire_inputs[0]
        # if owi and owi['value']:
        #     # append data
        #     logging.debug("Appending %s to temperature list", owi['value'])
        #     self.data_temperature.append(float(owi['value']))
        #     logging.debug(self.data_temperature)

    def store_data_csv(self):
        """ Store all collected data to csv file """
        logging.debug("Function store_data_csv")

        try:

            # date time
            now = datetime.now()

            # empty row
            row = ''
            date_time = now.strftime('%Y-%m-%d %H:%M:%S') # datetime

            logging.debug("Looping through digital inputs")
            row += "# digital inputs\n"
            for din in self.digital_inputs:
                logging.debug("Measure %s, id %s", din['name'], din['id'])

                # build row
                row += date_time + "\t"
                row += str(din['id']) + "\t" # id for database
                row += str(din['status']) + "\t" # channel status 1|0
                row += str(din['status_ev']) + "\t" # event status 1|0
                row += str(din['name']) + "\n" # channel name

            logging.debug("Looping through analog inputs")
            row += "# analog inputs\n"
            for ain in self.analog_inputs:
                logging.debug("Measure %s, id %s", ain['name'], ain['id'])

                # build row
                row += date_time + "\t"
                row += str(ain['id']) + "\t" # id
                if ain['value']:
                    row += str(round(ain['value'], 2)) + "\t" # channel values in volts
                else:
                    row += str(None) + "\t"
                row += str(ain['name']) + "\n" # channel name

            logging.debug("Looping through relay outputs")
            row += "# relay outputs\n"
            for rel in self.relay_outputs:
                logging.debug("Measure %s, id %s", rel['name'], rel['id'])

                # build row
                row += date_time + "\t"
                row += str(rel['id']) + "\t" # measure id for database
                row += str(rel['status']) + "\t" # channel status 1|0
                row += str(rel['name']) + "\n" # channel name

            logging.debug("Looping through open collector outputs")
            row += "# open collector outputs\n"
            for opc in self.open_collector_outputs:
                logging.debug("Measure %s, id %s", opc['name'], opc['id'])

                # build row
                row += date_time + "\t"
                row += str(opc['id']) + "\t" # measure id for database
                row += str(opc['status']) + "\t" # channel status 1|0
                row += str(opc['name']) + "\n" # channel name

            logging.debug("Looping through 1wire inputs")
            row += "# 1wire inputs\n"
            for owi in self.one_wire_inputs:
                logging.debug("Measure %s, id %s", owi['name'], owi['id'])

                # build row
                row += date_time + "\t"
                row += str(owi['id']) + "\t" # measure id for database
                if owi['value']:
                    row += str(round(owi['value'], 2)) + "\t" # channel value
                else:
                    row += str(None) + "\t"
                row += str(owi['name']) + "\n" # channel name

            # build daily file_name
            file_name = os.path.join(
                self.config['data_path'],
                self.config['file_header']+"_"+now.strftime('%Y-%m-%d')+".dat"
            ) # .%H%M

            # dump data to file
            logging.info("Saving data to file %s...", file_name)
            logging.debug("File row\n%s", row)
            with open(file_name, "a") as file:
                file.write(row)

            return True

        except Exception as ex:
            logging.error("An exception was encountered in store_data_csv: %s", str(ex))
            return False

    def store_ced_data_csv(self):
        """ Store 1 wire collected data to csv file for ced """
        logging.debug("Function store_ced_data_csv")

        try:
            if not self.data_temperature:
                logging.warning("No data found, data array is empty!")
                return False

            # get item
            logging.debug("Get 1wire first item")
            #item = self.analog_inputs[0]
            item = self.one_wire_inputs[0]
            if item is None:
                logging.warning("No item found!")
                return False
            # get database id
            dbid = item['db_id']

            # build row
            logging.debug("Build record")
            # date time
            now = datetime.now()
            row = now.strftime('%Y-%m-%d %H:%M:00') + "\t"
            # measure id for database
            row += str(dbid) + "\t"
            # average
            row += str(round(float(self._mean(self.data_temperature)), self.decimals)) + "\t"
            # min
            row += str(round(float(min(self.data_temperature)), self.decimals)) + "\t"
            # max
            row += str(round(float(max(self.data_temperature)), self.decimals)) + "\t"
            # stddev
            row += str(round(float(self._stddev(self.data_temperature)), self.decimals)) + "\n"

            # build daily file_name
            file_name = os.path.join(
                self.config['ftp_path'],
                self.config['file_header']+"_"+now.strftime('%Y-%m-%d')+".dat"
            ) # .%H%M

            # dump data to file
            logging.info("Saving data to file %s...", file_name)
            logging.debug("File row\n%s", row)
            with open(file_name, "a") as file:
                file.write(row)

            return True

        except Exception as ex:
            logging.error("An exception was encountered in store_ced_data_csv: %s", str(ex))
            return False

        finally:
            # reset array
            logging.info("Reset data array")
            self.data_temperature = []

    def parse_event(self, din):
        """ Parse event """
        # custom function for subclass to override
        logging.info("Function parse_event")

        try:

            # get status (on/off)
            logging.debug("GPIO %s, id %s, status %s",
                          din['name'], din['id'], din['status_ev'])

            # If AL_Door        > 0 Then alarm_cur = alarm_cur Or 1
            # If AL_Trafo       > 0 Then alarm_cur = alarm_cur Or 2
            # If AL_Free_2      > 0 Then alarm_cur = alarm_cur Or 4
            # If AL_ProbeFlux   > 0 Then alarm_cur = alarm_cur Or 8
            # If AL_Temp        > 0 Then alarm_cur = alarm_cur Or 16
            # If AL_PowerSupply > 0 Then alarm_cur = alarm_cur Or 128
            # If AL_Power       > 0 Then alarm_cur = alarm_cur Or 256

            if din['id'] == 1 and din['status_ev']: # Porta Aperta
                self.alarm_cur = self.alarm_cur | 1

            elif din['id'] == 2 and din['status_ev']: # Mancanza alimentazione
                self.alarm_cur = self.alarm_cur | 256

            elif din['id'] == 3 and din['status_ev']: # Temperatura elevata
                self.alarm_cur = self.alarm_cur | 16

            logging.debug("Current alarm: %s", self.alarm_cur)

            # store event
            self.store_event(din)

        except Exception as ex:
            logging.error("An exception was encountered in parse_event: %s", str(ex))

    def store_event(self, din):
        """ Store digital input event to file """
        logging.info("Function store_event")
        try:
            logging.debug("Digital input %s", din)

            if not din is None:

                now = datetime.now()
                # one hour back for timestamp
                #now = now - timedelta(hours=1)

                # empty row
                row = ''

                # build row
                row += now.strftime('%Y-%m-%d %H:%M:%S.%f') + "\t"
                row += str(din['id']) + "\t" # measure id for database
                row += str(din['status_ev']) + "\t" # channel status 1|0
                row += str(din['name']) + "\n" # channel name

                # build file_name
                logging.debug("Build file name")
                file_name = os.path.join(
                    self.config['data_path'],
                    self.config['file_header']+"_events_"+now.strftime('%Y-%m-%d')+".dat"
                )

                # dump data to file
                logging.debug("Saving data to file %s...", file_name)
                logging.debug("File row [%s]", row)
                with open(file_name, "a") as file:
                    file.write(row)

        except Exception as ex:
            logging.error("An exception was encountered in store_event: %s", str(ex))

    def analyze_alarm(self):
        """ Analyse alarm and send it if needed """
        logging.info("Function analyze_alarm")
        try:

            # self.alarm_cur = 0 # current alarm
            # self.alarm_old = 0
            # self.alarm_counter = 0
            # self.alarm_sent = False
            # self.alarm_door_sent = False

            self.alarm_cur = 0

            if self.digital_inputs[0]['status']: # Porta Aperta
                self.alarm_cur = self.alarm_cur | 1

            if self.digital_inputs[1]['status']: # Mancanza alimentazione
                self.alarm_cur = self.alarm_cur | 256

            if self.digital_inputs[2]['status']: # Temperatura elevata
                self.alarm_cur = self.alarm_cur | 16

            logging.debug("Current alarm: %s", self.alarm_cur)

            # if we sent an alarm and now is ok and counter > 1 hour we send
            # a reset message
            if self.alarm_sent and self.alarm_cur == 0 and self.alarm_counter >= self.alarm_send_reset_delay:

                # send http reset message as error = 0
                logging.debug("******************** RESET ALARM **********************")
                # send alarm
                thread = threading.Thread(target=self._send_alarm, daemon=True)
                thread.start()

                # reset flags
                self.alarm_sent = False
                self.alarm_counter = 0
                self.alarm_sent = False

            # send open door alarm if any and still not sent
            if (self.alarm_cur & 1) and not self.alarm_sent:

                # set flag
                self.alarm_sent = True

                # send http stuff
                logging.debug("+++++++++++++++++++++ DOOR ALARM +++++++++++++++++++++")
                thread = threading.Thread(target=self._send_alarm, daemon=True)
                thread.start()

                # set flag message sent
                self.alarm_sent = True

            # send alarm if any new - not door alarm
            if self.alarm_cur > 1 and (self.alarm_cur != self.alarm_old):

                # send http stuff
                logging.debug(">>>>>>>>>>>>>>>>>>>>>> NEW ALARM >>>>>>>>>>>>>>>>>>>>")
                thread = threading.Thread(target=self._send_alarm, daemon=True)
                thread.start()

                # set flag
                self.alarm_sent = True

            # increment the counter if an alarm has been sent
            if self.alarm_sent:
                self.alarm_counter = self.alarm_counter + self.config['polling_time'] # scan time

            # swap values new/old
            self.alarm_old = self.alarm_cur

        except Exception as ex:
            logging.error("An exception was encountered in analyze_alarm: %s", str(ex))
