#tft to pi connections
#tft pins --> pi pins
#led- --> ground
#led+ --> 3.3V
#skip next 4 pins
#cs --> 26 (ss)
#sca --> 23 (sck)
#sda --> 19 (mosi)
#a0 --> 11 (gpio; set command bit)
#reset --> 13 (gpio; reset hardware bit)
from time import sleep
import spidev
import RPi.GPIO as GPIO

#values for commands used for screen
SLPOUT = 0x11
COLMOD = 0x3A
DISPON = 0x29
CASET = 0x2A
RASET = 0x2B
RAMWR = 0x2C

bus = 0
device = 1
spi = spidev.SpiDev()
spi.open(bus, device)

spi.max_speed_hz = 62500000
spi.mode = 0

commandPin = 11
resetPin = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(commandPin, GPIO.OUT)
GPIO.setup(resetPin, GPIO.OUT)

def HardwareReset():
    #clear bit; GPIO;
    GPIO.output(resetPin, GPIO.LOW)
    sleep(.001)
    #set bit; GPIO;
    GPIO.output(resetPin, GPIO.HIGH)
    sleep(.2)

def WriteCommand(command):
    #clear bit; GPIO;
    commandToSend = [command]
    GPIO.output(commandPin, GPIO.LOW)
    spi.xfer2(commandToSend)
    #set bit; GPIO;
    GPIO.output(commandPin, GPIO.HIGH)

def InitDisplay():
    HardwareReset()
    WriteCommand(SLPOUT)
    sleep(.15)
    WriteCommand(COLMOD)
    spi.xfer2([0x05])
    WriteCommand(DISPON)

def WriteWord(word):
    spi.xfer2([word >> 8, word & 0x00FF])

def Write565(data, count):
    while(count > 0):
        spi.xfer2([data >> 8, data & 0x00FF])
        count = count - 1

def SetAddrWindow(x0, y0, x1, y1):
    WriteCommand(CASET)
    WriteWord(x0)
    WriteWord(x1)
    WriteCommand(RASET)
    WriteWord(y0)
    WriteWord(y1)

def DrawPixel(x, y, color):
    SetAddrWindow(x, y, x, y)
    WriteCommand(RAMWR)
    Write565(color, 1)

def FillRect(x0, y0, x1, y1, color):
    width = x1 - x0 + 1
    height = y1 - y0 + 1
    SetAddrWindow(x0, y0, x1, y1)
    WriteCommand(RAMWR)
    Write565(color, width * height)

def main():
    InitDisplay()
    color = 0x0000
    #fill screen using DrawPixel
    for i in range(128):
        for j in range(160):
            DrawPixel(i, j, color)
            color += 0x0010
        color += 0x0100
    sleep(4)
    for i in range(128):
        for j in range(160):
            DrawPixel(i, j, 0x0000)
    sleep(4)
    #make rectangles on screen using FillRect
    color = 0x041F
    FillRect(1, 1, 100, 100, color)
    color = 0x4014
    FillRect(1, 1, 100, 50, color)
    color = 0xF81F
    FillRect(1, 1, 50, 100, color)
    sleep(4)

if __name__ == '__main__':
    main()
