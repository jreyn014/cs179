#connections between tft and pi
#tft pins --> pi pins
#led- --> ground
#led+ --> 3.3V
#cs --> 26 (ss)
#sca --> 23 (sck)
#sda --> 19 (mosi)
#a0 --> 11 (gpio; set command bit)
#reset --> 13 (gpio; reset hardware bit)
from time import sleep
import spidev
import RPi.GPIO as GPIO

#values used for screen
SLPOUT = [0x11]
COLMOD = [0x3A]
DISPON = [0x29]

bus = 0
device = 1
spi = spidev.SpiDev()
spi.open(bus, device)

spi.max_speed_hz = 500000
spi.mode = 0

commandPin = 11
resetPin = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(commandPin, GPIO.OUT)
GPIO.setup(resetPin, GPIO.OUT)

def HardwareReset():
#    clear bit; GPIO; different than WC
    GPIO.output(resetPin, GPIO.LOW)
    sleep(.001)
#    set bit; GPIO; different than WC
    GPIO.output(resetPin, GPIO.HIGH)
    sleep(.2)

def WriteCommand(command):
#    clear bit; GPIO; different than HWR
    GPIO.output(commandPin, GPIO.LOW)
    spi.xfer2(command)
#    set bit; GPIO; different than HWR
    GPIO.output(commandPin, GPIO.HIGH)

def InitDisplay():
    HardwareReset()
    WriteCommand(SLPOUT) #find value in datasheet
#    WriteCommand([0x11])
    sleep(.15)
    WriteCommand(COLMOD) #find value in datasheet
#    write byte???
    spi.xfer2([0x05])
    WriteCommand(DISPON) #find value in datasheet
    print("done")

def main():
    #spi.xfer2()
    InitDisplay()

    GPIO.cleanup()

if __name__ == '__main__':
    main()
