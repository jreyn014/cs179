import RPi.GPIO as GPIO

def button_callback(channel):
    print("pressed")

buttonPin = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#outputs pressed while button is pressed
#while 1:
#    if GPIO.input(buttonPin) == GPIO.HIGH:
#        print("pressed")

#outputs pressed every time a rising edge is detected during button press
GPIO.add_event_detect(buttonPin, GPIO.RISING, callback = button_callback)

message = input("Press enter to quit\n\n")

GPIO.cleanup()

