import globals
from enum import Enum
import random
import copy
import screen

Blocks = {
    'I' : [
    ['.','.','.','.'],
    ['I','I','I','I'],
    ['.','.','.','.'],
    ['.','.','.','.']
    ],

    'O' : [
    ['.','.','.','.'],
    ['.','O','O','.'],
    ['.','O','O','.'],
    ['.','.','.','.']
    ],

    'J' : [
    ['.','.','.'],
    ['J','J','J'],
    ['.','.','J'],
    ],

    'L' : [
    ['.','.','.'],
    ['L','L','L'],
    ['L','.','.'],
    ],

    'S' : [
    ['.','.','.'],
    ['.','S','S'],
    ['S','S','.']
    ],

    'Z' : [
    ['.','.','.'],
    ['Z','Z','.'],
    ['.','Z','Z']
    ],

    'T' : [
    ['.','.','.'],
    ['T','T','T'],
    ['.','T','.']
    ]
}

class Block:

    def __init__(self,key = None):
        if key:
            self.key = key
        else:
            self.key = random.choice(list(Blocks.keys()))
        self.block = Blocks[self.key]
        self.n = len(self.block[0])
        self.index = [0,4] #Top left of n x n block
    
    def move_Left(self):
        B = copy.deepcopy(self)
        B.index[1] -= 1
        return B
    #end def move_Left
    
    def move_Right(self):
        B = copy.deepcopy(self)
        B.index[1] += 1
        return B
    #end def move_Right
    
    def move_Down(self):
        B = copy.deepcopy(self)
        B.index[0] += 1
        return B
    #end def move_Down
    
    def rotate_CW(self):
        B = copy.deepcopy(self)
        block = B.block
        n = B.n
        for x in range(0, (int(n/2))):
            for y in range(x, n-x-1):
                T =  block[n-1-y][x]
                block[n-1-y][x] = block[n-1-x][n-1-y]
                block[n-1-x][n-1-y] = block[y][n-1-x]
                block[y][n-1-x] = block[x][y]
                block[x][y] = T
        return B
    #end def rotate_CW
    
    def rotate_ACW(self):
        B = copy.deepcopy(self)
        block = B.block
        n = B.n
        for x in range(0, (int(n/2))):
            for y in range(x, n-x-1):
                T = block[x][y]
                block[x][y] = block[y][n-1-x]
                block[y][n-1-x] = block[n-1-x][n-1-y]
                block[n-1-x][n-1-y] = block[n-1-y][x]
                block[n-1-y][x] = T
        return B
    #end def rotate_ACW
    
    def print_Block(self):
        B = copy.deepcopy(self)
        n = B.n
        if n == 3:
            for row in B.block:
                row.append('.')
            B.block.append(['.','.','.','.'])
        return B.block
#end class Block

def isCollision(m,b):
    (row,column) = b.index
    n = b.n
    for i in range(n):
        for j in range(n):
            if b.block[i][j] != '.':
                if m.map[row+i][column+j] != '.':
                    return True #collision detected
    
    return False #no collision
#end def

class Map:
    def __init__(self):
        self.map = [
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['>','.','.','.','.','.','.','.','.','.','.','<'],
        ['^','^','^','^','^','^','^','^','^','^','^','^']]
    #end def __init__
    
    def set(self,B):
        (row,column) = B.index
        n = B.n
        new_map = copy.deepcopy(self)
        for i in range(n):
            for j in range(n):
                if B.block[i][j] != '.':
                    new_map.map[row+i][column+j] = B.block[i][j]
        return new_map
    #end def
    
    def checkLines(self):
        map = self.map
        full_lines = []
        for row in range(21):
            full = True
            for column in range(1,11):
                if map[row][column] == '.':
                    full = False
                    break
            if full:
                full_lines.append(row)
        if len(full_lines) > 0:     
            for row in full_lines:
                for column in range(1,11):
                    map[row][column] = '='
        return len(full_lines)
    #end def
    
    def print_Map(self):
        nothing = 0
#        for row in self.map:
#            for column in row:
#                print(column,end=' ')
#            print()
#end class Map
        

States = Enum('States', 'init GAME_OFF GAME_ON')
state = States.init
game_map = Map()
active_block = Block()
next_block = Block()
hold_block = Block()
hold_latch = False
lines = [0,0,0,0]
button_latch = {
"A"     : False, 
"B"     : False, 
"Up"    : False, 
"Down"  : False, 
"Left"  : False, 
"Right" : False
}
autodown_count = 0
speed = 1
clear_lines = False
clear_count = 0

def tick():
    global state
    global game_map
    global active_block
    global next_block
    global hold_block
    global hold_latch
    global lines
    global button_latch
    global autodown_count
    global speed
    global clear_lines
    global clear_count
    
    #Transitions
    if state == States.init:
        state = States.GAME_OFF
        
    elif state == States.GAME_OFF:
        if globals.game_play == True:
            game_map = Map()
            active_block = Block()
            next_block = Block()
            hold_block = Block()
            lines = [0,0,0,0]
            for button in button_latch:
                button_latch[button] = False
            autodown_count = 0
            speed = 1
            clear_lines = False
            clear_count = 0
            screen.SetupGameScreen()
            state = States.GAME_ON
        else:
            state == States.GAME_OFF
        
    elif state == States.GAME_ON:
        if globals.game_play == True:
            state = States.GAME_ON
        else:
            state = States.GAME_OFF
        
    else:
        state = States.init
        
    #Actions
    if state == States.init:
        pass
    elif state == States.GAME_OFF:
        pass
    elif state == States.GAME_ON:
        buttons = globals.buttons
        test_block = active_block
        
        #Unlatch Inputs
        for button in button_latch:
            if not buttons[button]:
                button_latch[button] = False
        
        #Check Buttons
        if buttons["Up"] and not button_latch["Up"] and not hold_latch:         #Hold block
            button_latch["Up"] = True
            hold_latch = True
            temp = copy.deepcopy(hold_block)
            test_block.index = [0,4]
            hold_block = Block(test_block.key)
            test_block = Block(temp.key)
            autodown_count = 0
        
        if buttons["A"] and not button_latch["A"]:           #Rotate Anticlockwise
            button_latch["A"] = True
            test_block = active_block.rotate_ACW()
            
        if buttons["B"] and not button_latch["B"]:           #Rotate Clockwise
            button_latch["B"] = True
            test_block = active_block.rotate_CW()
            
        if buttons["Left"] and not button_latch["Left"]:     #Move Left
            button_latch["Left"] = True
            test_block = active_block.move_Left()
            
        if buttons["Right"] and not button_latch["Right"]:   #Move Right
            button_latch["Right"] = True
            test_block = active_block.move_Right()
        
        if not isCollision(game_map,test_block):
            active_block = test_block
        
        #Check downward movement
        if ( buttons["Down"]  and not button_latch["Down"] ) or autodown_count >= 20:    #Move Down
            button_latch["Down"] = True if buttons["Down"] else False
            test_block = active_block.move_Down()
            if not isCollision(game_map,test_block):
                active_block = test_block
            else:
                game_map = game_map.set(active_block)
                clear_lines = game_map.checkLines()
                active_block = Block(next_block.key)
                next_block = Block()
                hold_latch = False
                if isCollision(game_map,active_block):
                    globals.game_play = False   #GAME OVER
            autodown_count = 0
        else:
            autodown_count += sum(lines)/10 + 1
        
        #Check lines
        if clear_lines > 0:
            if clear_count >=10:
                for row in range(21):
                    if game_map.map[row][1] == '=':
                        game_map.map.pop(row)
                        game_map.map.insert(0,['>','.','.','.','.','.','.','.','.','.','.','<'])
                lines[clear_lines-1] = lines[clear_lines-1] + 1
                clear_count = 0
                clear_lines = 0
            else:
                clear_count += sum(lines)/20 + 1
        
        globals.hold_block = hold_block
        globals.hold_block.print_Block()
        globals.game_map = game_map.set(active_block)
        globals.game_map.print_Map()
        globals.next_block = next_block
        globals.next_block.print_Block()
        for i in range(4):
            globals.lines[i] = lines[i]
            
        screen.MainGame()
        screen.NextBlock()
        screen.HeldBlock()
        screen.UpdateLines()
#end def tick