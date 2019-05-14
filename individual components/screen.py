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
import screen_characters

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
    Write565(~color, 1)

def FillRect(x0, y0, x1, y1, color):
    width = x1 - x0 + 1
    height = y1 - y0 + 1
    SetAddrWindow(x0, y0, x1, y1)
    WriteCommand(RAMWR)
    Write565(~color, width * height)

def ColorLUT(inputChar):
    if inputChar == '.':
        return 0x738E
    elif inputChar == 'T':
        return 0x94C0
    elif inputChar == 'S':
        return 0x0B6B
    elif inputChar == 'I':
        return 0xFFFF
    elif inputChar == 'O':
        return 0x0012
    elif inputChar == 'J':
        return 0x0B80
    elif inputChar == 'L':
        return 0x8010
    elif inputChar == 'Z':
        return 0x6800
    elif inputChar == '>':
        return 0x0000
    elif inputChar == '<':
        return 0x0000
    elif inputChar == '=':
        return 0x0000
    elif inputChar == '^':
        return 0x0000


def SetupGameScreen():
    FillRect(0, 0, 127, 159, ~0xFFFF)#0x31A6)

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
    FillRect(8,13,77,159,0x738E)

def DrawSquare(x0,y0,x1,y1,color):
    if x1 < x0:
        t = x1
        x1 = x0
        x0 = t
    if y1 < y0:
        t = y1
        y1 = y0
        y0 = t
    FillRect(x0,y0,x1,y0,ColorLUT(color))
    FillRect(x1,y0+1,x1,y1,ColorLUT(color))
    FillRect(x1-1,y1,x0,y1,ColorLUT(color))
    FillRect(x0,y1-1,x0,y0+1,ColorLUT(color))
    FillRect(x0+1,y0+1,x1-1,y1-1,ColorLUT(color))


def MainGame():
    if globals.game_map != None:
        if globals.game_map_old == None:
#            FillRect(8, 13, 77, 159, 0xFFFF)
            for i in range(1,11):
                for j in range(21):
                    DrawSquare(7*i,7*j,7*i+6,7*j+6,globals.game_map.map[j][i])
                    #FillRect(7 * i, 7 * j, 7 * i + 6, 7 * j + 6, ColorLUT(globals.game_map.map[j][i]))
            offsetX = 92
            LetterSize = 6
            for i in range(5):
                for j in range(5):
                    DrawPixel(i + offsetX, j + 35, ColorLUT(screen_characters.N[j][i]))
                    DrawPixel(i + offsetX + LetterSize, j + 35, ColorLUT(screen_characters.E[j][i]))
                    DrawPixel(i + offsetX + 2 * LetterSize, j + 35, ColorLUT(screen_characters.X[j][i]))
                    DrawPixel(i + offsetX + 3 * LetterSize, j + 35, ColorLUT(screen_characters.T[j][i]))

                    DrawPixel(i + offsetX, j + 80, ColorLUT(screen_characters.H[j][i]))
                    DrawPixel(i + offsetX + LetterSize, j + 80, ColorLUT(screen_characters.O[j][i]))
                    DrawPixel(i + offsetX + 2 * LetterSize, j + 80, ColorLUT(screen_characters.L[j][i]))
                    DrawPixel(i + offsetX + 3 * LetterSize, j + 80, ColorLUT(screen_characters.D[j][i]))
        else:
            for i in range(1,11):
                for j in range(21):
                    if globals.game_map_old.map[j][i] != globals.game_map.map[j][i]:
                        DrawSquare(7*i,7*j,7*i+6,7*j+6,globals.game_map.map[j][i])
                        #FillRect(7 * i, 7 * j, 7 * i + 6, 7 * j + 6, ColorLUT(globals.game_map.map[j][i]))
        globals.game_map_old = copy.deepcopy(globals.game_map)

def NextBlock():
    if globals.next_block != None:
        next_block = globals.next_block.print_Block()
        offsetX = 92
        offsetY = 4
        if globals.next_block_old != None:
            for i in range(4):
                for j in range(4):
                    if next_block[j][i] != globals.next_block_old[j][i]:
                        DrawSquare(7* i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, next_block[j][i])
                        #FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.next_block.block[j][i]))
        else:
            for i in range(4):
                for j in range(4):
                    DrawSquare(7* i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, next_block[j][i])
                    #FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.next_block.block[j][i]))
        globals.next_block_old = copy.deepcopy(next_block)

def HeldBlock():
    if globals.hold_block != None:
        hold_block = globals.hold_block.print_Block()
        offsetX = 92
        offsetY = 50
        if globals.hold_block_old != None:
#            hold_block_old = globals.hold_block_old.print_Block()
            for i in range(4):
                for j in range(4):
                    if hold_block[j][i] != globals.hold_block_old[j][i]:
                        DrawSquare(7* i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, hold_block[j][i])
                        #FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.hold_block.block[j][i]))
        else:
            for i in range(4):
                for j in range(4):
                    DrawSquare(7* i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, hold_block[j][i])
                    #FillRect(7 * i + offsetX, 7 * j + offsetY, 7 * i + 6 + offsetX, 7 * j + 6 + offsetY, ColorLUT(globals.hold_block.block[j][i]))
        globals.hold_block_old = copy.deepcopy(hold_block)
