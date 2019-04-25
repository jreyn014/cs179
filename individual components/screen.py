from time import sleep
import spidev # as spi
import RPi.GPIO as GPIO

#values for commands used for screen
SLPOUT = [0x11]
COLMOD = [0x3A]
DISPON = [0x29]
CASET = [0x2A]
RASET = [0x2B]
RAMWR = [0x2C]

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

def Write565(data, count):
    while(count > 0):
        spi.xfer2([data >> 8])
        spi.xfer2([data & 0xFF])
        count = count - 1

def SetAddrWindow(x0, y0, x1, y1):
    WriteCommand(CASET) #find value in datasheet
    #WriteWord(x0)
    spi.xfer2([x0 >> 8, x0 & 0xFF])
    #WriteWord(x1)
    spi.xfer2([x1 >> 8, x1 & 0xFF])
    WriteCommand(RASET) #find value in datasheet
    #WriteWord(y0)
    spi.xfer2([y0 >> 8, y0 & 0xFF])
    #WriteWord(y1)
    spi.xfer2([y1 >> 8, y1 & 0xFF])

def DrawPixel(x, y, color):
    SetAddrWindow(x, y, x, y)
    WriteCommand(RAMWR) #find value in datasheet
    Write565(color, 1)

def main():
    #spi.xfer2()
    InitDisplay()
    
    for i in range(200):
        for j in range(200):
            DrawPixel(i, j, 0xFFFF)

    GPIO.cleanup()

if __name__ == '__main__':
    main()
