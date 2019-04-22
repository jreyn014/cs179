import RPi.GPIO as GPIO
from time import sleep

def button_pressed():
    global state
    if state == 0:
        #button not pressed
        if GPIO.input(buttonPin) == GPIO.HIGH:
            print("pressed")
            state = 1
        else:
            state = 0
    elif state == 1:
        #button pressed
        if GPIO.input(buttonPin) == GPIO.HIGH:
            state = 1
        else:
            state = 0
    else:
        state = 0;

buttonPin = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

state = 0

while 1:
    sleep(.050)
    button_pressed()

GPIO.cleanup()

