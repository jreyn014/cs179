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

#maybe try spi.xfer()???

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
#spi.max_speed_hz = 50000000
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
#    commandToSend = [str(command)]
    commandToSend = [command]
    GPIO.output(commandPin, GPIO.LOW)
    spi.xfer2(commandToSend)
#    set bit; GPIO; different than HWR
    GPIO.output(commandPin, GPIO.HIGH)
#    print("command = " + hex(command))
#    print("commandToSend[0] = " + hex(commandToSend[0]))

def InitDisplay():
    HardwareReset()
    WriteCommand(SLPOUT) #find value in datasheet
    sleep(.15)
    WriteCommand(COLMOD) #find value in datasheet
    spi.xfer2([0x05])
    WriteCommand(DISPON) #find value in datasheet
    print("done")

def WriteWord(word):
    #spi.xfer2([word >> 8])
    #spi.xfer2([word & 0x00FF])
    #spi.xfer2([word >> 8, word & 0x00FF])
    spi.xfer2([word])
#    print("word >> 8 = " + hex(word >> 8) + ", word & 0x00FF = " + hex(word & 0x00FF))

def Write565(data, count):
    while(count > 0):
        #spi.xfer2([data >> 8])
        #spi.xfer2([data & 0x00FF])
        spi.xfer2([data >> 8, data & 0x00FF])
        #WriteWord(data)
        count = count - 1

def SetAddrWindow(x0, y0, x1, y1):
    WriteCommand(CASET) #find value in datasheet
    WriteWord(x0)
    WriteWord(x1)
    WriteCommand(RASET) #find value in datasheet
    WriteWord(y0)
    WriteWord(y1)

def DrawPixel(x, y, color):
    SetAddrWindow(x, y, x, y)
    WriteCommand(RAMWR) #find value in datasheet
    Write565(color, 1)

def FillRect(x0, y0, x1, y1, color):
    width = x1 - x0 + 1
    height = y1 - y0 + 1
    SetAddrWindow(~x0, ~y0, ~x1, ~y1)
    WriteCommand(RAMWR)
    Write565(color, width * height)

def main():
    #spi.xfer2()
    InitDisplay()
    color = 0x0000
    for i in range(128):
        for j in range(160):
            DrawPixel(i, j, color)
            color += 0x0010
        color += 0x0100
    sleep(4)
    color = 0x041F
    FillRect(1, 1, 50, 100, color)
    sleep(1)
    color = 0x4014
    FillRect(1, 1, 100, 50, color)
    sleep(1)
    color = 0xF81F
    FillRect(1, 1, 100, 100, color)
    sleep(4)
#    for i in range(28):
#        for j in range(28):
#            DrawPixel(i, j, color)
#    sleep(4)
#    color = 0x0000
#    for i in range(28):
#        for j in range(28):
#            DrawPixel(i, j, color)
#    sleep(4)
#    color = 0x0FF0
#    for i in range(28):
#        for j in range(28):
#            DrawPixel(i, j, color)
#    sleep(4)
    #GPIO.cleanup()

if __name__ == '__main__':
    main()
