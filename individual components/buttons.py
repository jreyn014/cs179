import RPi.GPIO as GPIO
import globals
from enum import Enum
#import keyboard #Test import

#Replace with GPIO pins
#change get key
A = 33
B = 35
up = 36
down = 37
left = 38
right = 40

buttons = {
A     : "A",
B     : "B",
up    : "Up",
down  : "Down",
left  : "Left",
right : "Right"
}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(A, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(B, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(up, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(down, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(left, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(right, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


States = Enum('States', 'init POLL')
state = States.init

#cmd line testing functions
def getKey(key):
    try:
#        if keyboard.is_pressed(key):
        if GPIO.input(key):
            return True
        else:
            return False
    except Exception as er:
        return False

def tick():
    global state
    #Transitions
    if state == States.init:
        for button in globals.buttons:
            globals.buttons[button] = False
        state = States.POLL
    elif state == States.POLL:
        state = States.POLL
    else:
        state = 0
    
    #Actions
    if state == States.init:
        pass
    elif state == States.POLL:
        for button in buttons:
            globals.buttons[buttons[button]] = True if getKey(button) else False
        
