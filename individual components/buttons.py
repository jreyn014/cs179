#import RPi.GPIO as GPIO
import globals
from enum import Enum
import keyboard #Test import
#Buttons:
#A, B, up, down, left, right

#Replace with GPIO pins
A = "z"
B = "x"
up = "w"
down = "s"
left = "a"
right = "d"

buttons = [A,B,up,down,left,right]

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
        globals.buttons = [False, False, False, False, False, False]
        state = States.POLL
    elif state == States.POLL:
        state = States.POLL
    else:
        state = 0
    
    #Actions
    if state == States.init:
        pass
    elif state == States.POLL:
        for i in range(len(buttons)):
            #Change getKey to GPIO.HIGH
            globals.buttons[i] = True if getKey(buttons[i]) else False
        