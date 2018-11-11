#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import signal
import time
from Queue import Queue

from MFRC522 import MFRC522

continue_reading = True
timeout = 3 # 3 seconds
pi_id = '41056'

def after_pump(arg):
    print "Pump from # {}".format(arg)
    print "Card: {}".format(Scanners[Pumps[arg]]['card_id'])
    for scanner in Scanners:
        print "{}-{} card:{}, lastscan:{}".format(pi_id, scanner['scanner_id'], scanner['card_id'], scanner['last_scanned'])

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    print "Dumping Scanner values:"

    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create a list of MFRC522 objects
MIFAREReaders = []
MIFAREReaders.append(MFRC522(dev='/dev/spidev1.0', rst=18))
MIFAREReaders.append(MFRC522())

# Create a list of Scanners (to be associated with each MIFAREReader)
Scanners = [
        {'scanner_id': '1', 'card_id': '', 'last_scanned': time.time(), 'pump_pin': 15},
        {'scanner_id': '2', 'card_id': '', 'last_scanned': time.time(), 'pump_pin': 16}
]

# Create another mapping between Pumps and Scanners
Pumps = { 15: 0, 16: 1 }

# Set the GPIO pins
GPIO.setmode(GPIO.BOARD)
for scanner in Scanners:
    pin = scanner['pump_pin']
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING)
    GPIO.add_event_callback(pin, after_pump)

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Poll the scanners

    for (ndx, MIFAREReader) in enumerate(MIFAREReaders):

        # Cleanup timeout cards
        scanner = Scanners[ndx]
        if time.time() - scanner['last_scanned'] > timeout:
            scanner['card_id'] = ''

        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected from Reader"
        else:
            continue

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll_String()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            #print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
            print "Card read UID: %s" % (uid)
            Scanners[ndx]['card_id'] = uid
            Scanners[ndx]['last_scanned'] = time.time()

