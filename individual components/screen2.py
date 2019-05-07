import RPi.GPIO as GPIO
import time

A0 = 26 
SDAT = 6  
SCK = 13 

#commands:
SWRESET = 0x01
SLPOUT = 0x11
DISPON = 0x29
CASET = 0x2A
RASET = 0x2B
RAMWR = 0x2C
MADCTL = 0x36
COLMOD = 0x3A

def SetPin(pinNumber,value):
	GPIO.output(pinNumber,value)

def initIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(A0,GPIO.OUT)
	GPIO.setup(SDAT,GPIO.OUT)
	GPIO.setup(SCK,GPIO.OUT)
	GPIO.output(SCK,0)

def Clk():
	SetPin(SCK, 1)
	SetPin(SCK, 0)

def WriteByte(value, data=True):
	mask = 0x80
	SetPin(A0, data)
	for bit in range(8):
		SetPin(SDAT,value & mask)
		Clk()
		mask >>= 1

def WriteCmd(value):
	WriteByte(value, False)

def WriteWord(value):
	WriteByte(value >> 8)
	WriteByte(value & 0xFF)

def WriteList(bytes):
	for byte in bytes:
		WriteByte(byte)

def InitDisplay():
	WriteCmd(SWRESET)
	time.sleep(0.2)
	WriteCmd(SLPOUT)
	time.sleep(0.2)
	WriteCmd(COLMOD)
	WriteByte(0x05)	
	time.sleep(0.2)
	WriteCmd(DISPON)

def Write888(value,reps=1):
	green = value>>8
	blue = value & 0xFF
	RGB = [green, blue]
	for a in range(reps):
		WriteList(RGB)

def SetAddrWindow(x0, y0, x1, y1):
	WriteCmd(CASET)
	WriteWord(x0)
	WriteWord(x1)
	WriteCmd(RASET)
	WriteWord(y0)
	WriteWord(y1)

def WriteColor(color, reps=1):
	WriteCmd(RAMWR)
	Write888(color, reps)	

initIO()
InitDisplay()
SetAddrWindow(0,0,99,99)
WriteColor(0x0FF0,100*100)
SetAddrWindow(0,100,127,159)
WriteColor(0xF00F,128*60)
SetAddrWindow(100,0,127,99)
WriteColor(0x0000,28*100)

print "done"
