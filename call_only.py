#!/usr/bin/env python

"""\
Demo: handle incoming calls
Simple demo app that listens for incoming calls, displays the caller ID,
optionally answers the call and plays sone DTMF tones (if supported by modem),
and hangs up the call.
Incoming calls and messages incoming are written to /var/log/messages by default. for Content gotta visit AT commands.
"""

from __future__ import print_function
from subprocess import os
import time, logging
import numpy as np
import matplotlib.pyplot as plt
PORT = '/dev/ttyAMA0' # Where the device is connected to RX and TX pins from raspberry pi
BAUDRATE = 9600
PIN = "" # SIM card PIN 

from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))

def main():
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = False
    modem.connect(PIN)
    print('Waiting for SMS message...')
    try:
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close();

if __name__ == '__main__':
    main()
