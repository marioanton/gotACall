#!/usr/bin/env python

"""\
Demo: handle incoming calls
Simple demo app that listens for incoming calls, displays the caller ID,
optionally answers the call and plays sone DTMF tones (if supported by modem),
and hangs up the call.
"""

from __future__ import print_function
from subprocess import os
import time, logging
import numpy as np
import matplotlib.pyplot as plt
PORT = '/dev/ttyUSB0'
BAUDRATE = 9600
PIN = 9683 # SIM card PIN (if any)

from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException

def handleIncomingCall(call):
    logging.basicConfig(filename='/var/log/gsm.log', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    print('Incoming call from:', call.number)
    caller =  "Mario, te esta llamando el siguiente numero: " +  str(call.number)
    cmd = "/home/pi/Desktop/yowsup/yowsup/yowsup-cli demos -l 44XXXXXXXXX:pass -s 34XXXXXXXXX " + "'" +  caller + "'"
    print (cmd)
    logging.info(call.number)
    os.system(cmd)
    mensaje = " Te devuelo la llamada rapido - Mario"
    if call.number != None:
	    cmd = "/home/pi/Desktop/yowsup/yowsup/yowsup-cli demos -l 44XXXXXXXXX:pass= -s 34" +  str(call.number)  + " '" +  mensaje + "'"
	    logging.warning(cmd)
	    print (cmd)
	    os.system(cmd)
    if call.ringCount == 10000:
	    print('Incoming call from:', call.number)
            print('Answering call and playing some DTMF tones...')
            call.answer()
            # Wait for a bit - some older modems struggle to send DTMF tone immediately after answering a call
            time.sleep(2.0)
            try:
                call.sendDtmfTone('11111111')
            except InterruptedException as e:
                # Call was ended during playback
                print('DTMF playback interrupted: {0} ({1} Error {2})'.format(e, e.cause.type, e.cause.code))
            finally:
                if call.answered:
                    print('Hanging up call.')
                    call.hangup()
    else:
        print(' Call from {0} is still ringing...'.format(call.number))
      #  tones =  "Mario, tono : " +  str(call.ringCount) + " - Phone Number -" + str(call.number)
      #  cmd = "/home/pi/Desktop/yowsup/yowsup/yowsup-cli demos -l 44XXXXXXXXX:pass= -s 34XXXXXXXXX " + "'" +  tones + "' >> /var/log/wsup  2>&1"
      #  os.system(cmd)
def main():
    print('Initializing modem...')
    logging.basicConfig(filename='/var/log/gsm.log', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, incomingCallCallbackFunc=handleIncomingCall)
    modem.connect()
    print('Waiting for incoming calls...')
    try:
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close()

if __name__ == '__main__':
    main()
