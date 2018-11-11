'''
We're going to use able and baker as names for the scanners.

States of the machine
0: Idle
1: Scanned, Waiting Pump
2: Got Pump, sent response
3: Pumped, Sent to database
4: Error
5:

'''
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def cardscan():
    return "scanned"

'''
def state_control(state, button, pump):
    if state == 0:
        if scanner_able = scans:
            card_able = cardscan()
            if pump == 0:
                time_able = time()
            elif pump == 1:
                time_baker = time()
            return 2
    elif state == 1: #give 5 seconds buffer
        if pump == 0:
            time_pump = time_able
        elif pump == 1:
            time_pump = time_baker
        if time() - time_pump > 5.0:
            #LED TIMEOUT
            return 0;
        if GPIO.input(button) == GPIO.HIGH:
            return 2
    elif state == 2:
        #SEND THE DATA
        return 0
'''

def after_pump(arg):
    print "asdf"
    print arg

'''
Pins
'''

#init
state_able = 0
state_baker = 0
button_able = 23
button_baker = 26
card_able = ''
card_baker = ''
time_able = 0
time_baker = 0

# Add callback

GPIO.add_event_detect(button_able, GPIO.RISING)
GPIO.add_event_callback(button_able, after_pump)

#loop forever
x = 3
while(True):
    #state_able = state_control(state_able, button_able, 0)
    x = 4
