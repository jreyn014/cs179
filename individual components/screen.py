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
import time
import spidev
import RPi.GPIO as GPIO
import copy

import globals

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

def ColorLUT(inputChar):
    if inputChar == '.':
        return 0xFFFF
    elif inputChar == 'T':
        return 0x000F
    elif inputChar == 'S':
        return 0x00F0
    elif inputChar == 'I':
        return 0x0F00
    elif inputChar == 'O':
        return 0xF000
    elif inputChar == 'J':
        return 0x00FF
    elif inputChar == 'L':
        return 0x0FF0
    elif inputChar == 'Z':
        return 0xFF00
    elif inputChar == '>':
        return 0x0000
    elif inputChar == '<':
        return 0x0000
    elif inputChar == '=':
        return 0x0000
    elif inputChar == '^':
        return 0x0000

def SetupGameScreen():
    FillRect(0, 0, 127, 159, 0xFFFF)

def DrawBricks():
    Fill_Color = 0xDEBD
    Outline_Color = 0x2965
    FillRect(0,0,84,159,Fill_Color)
    for i in range(80):
	FillRect(0,i*2,84,i*2,Outline_Color)
    	if (i % 2) == 0:
	    for j in range(1,22):
		DrawPixel(j*4-1,i+1,Outline_Color)
	else:
	    for k in range(1,22):
		DrawPixel(j*4-3,i+1,Outline_Color)

def MainGame():
    if globals.game_map != None:
        if globals.game_map_old == None:
            for i in range(12):
                for j in range(22):
                    FillRect(7 * i, 7 * j, 7 * i + 6, 7 * j + 6, ColorLUT(globals.game_map.map[j][i]))
        else:
            for i in range(12):
                for j in range(21):
                    if globals.game_map_old.map[j][i] != globals.game_map.map[j][i]:
                        FillRect(7 * i, 7 * j, 7 * i + 6, 7 * j + 6, ColorLUT(globals.game_map.map[j][i]))
        globals.game_map_old = copy.deepcopy(globals.game_map)

def NextBlock():
    if globals.next_block != None:
        offsetX = 92
        offsetY = 4
        if globals.next_block_old != None:
            for i in range(3):
                for j in range(3):
                    if globals.next_block.block[j][i] != globals.next_block_old.block[j][i]:
                        FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.next_block.block[j][i]))
        else:
            for i in range(3):
                for j in range(3):
                        FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.next_block.block[j][i]))
        globals.next_block_old = copy.deepcopy(globals.next_block)

def HeldBlock():
    if globals.hold_block != None:
        offsetX = 92
        offsetY = 32
        if globals.hold_block_old != None:
            for i in range(3):
                for j in range(3):
                    if globals.hold_block.block[j][i] != globals.hold_block_old.block[j][i]:
                        FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.hold_block.block[j][i]))
        else:
            for i in range(3):
                for j in range(3):
                    FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.hold_block.block[j][i]))
        globals.hold_block_old = copy.deepcopy(globals.hold_block)
