#import RPi.GPIO as GPIO
import globals
from enum import Enum
import keyboard #Test import

#Replace with GPIO pins
A = "z"
B = "x"
up = "w"
down = "s"
left = "a"
right = "d"

buttons = {
A     : "A",
B     : "B",
up    : "Up",
down  : "Down",
left  : "Left",
right : "Right"
}

States = Enum('States', 'init POLL')
state = States.init

#cmd line testing functions
def getKey(key):
    try:
        if keyboard.is_pressed(key):
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
        