import globals
from enum import Enum
import random
import copy

A = 0; B = 1; up = 2; down = 3; left = 4; right = 5;

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

    def __init__(self):
        self.block = Blocks[random.choice(list(Blocks.keys()))]
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
        B = self.block
        n = self.n
        for row in range(n):
            for column in range(n):
                print(B[row][column],end=' ')
            print()
        print()
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
        for row in self.map:
            for column in row:
                print(column,end=' ')
            print()
#end class Map
        

States = Enum('States', 'init GAME_OFF GAME_ON')
state = States.init
game_map = Map()
active_block = Block()
next_block = Block()
held_block = Block()
lines = [0,0,0,0]
#               A      B      up     down   left   right
button_latch = [False, False, False, False, False, False]
autodown_count = 0
speed = 1
clear_lines = False
clear_count = 0

def tick():
    global state
    global game_map
    global active_block
    global next_block
    global held_block
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
            held_block = Block()
            lines = [0,0,0,0]
            #               A      B      up     down   left   right
            button_latch = [False, False, False, False, False, False]
            autodown_count = 0
            speed = 1
            clear_lines = False
            clear_count = 0
            state = States.GAME_ON
        else:
            state == States.GAME_OFF
        
    elif state == States.GAME_ON:
        if globals.game_play == True:
            state = States.GAME_ON
        else:
            print("Game Over")
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
        for button in range(6):
            if not buttons[button]:                     #Unlatch inputs
                button_latch[button] = False
                
        if buttons[up] and not button_latch[up]:         #Hold block
            button_latch[up] = True
            temp = copy.deepcopy(held_block)
            test_block.index = [0,4]
            held_block = copy.deepcopy(test_block)
            test_block = copy.deepcopy(temp)
        
        if buttons[A] and not button_latch[A]:           #Rotate Anticlockwise
            button_latch[A] = True
            test_block = active_block.rotate_ACW()
            
        if buttons[B] and not button_latch[B]:           #Rotate Clockwise
            button_latch[B] = True
            test_block = active_block.rotate_CW()
            
        if buttons[left] and not button_latch[left]:     #Move Left
            button_latch[left] = True
            test_block = active_block.move_Left()
            
        if buttons[right] and not button_latch[right]:   #Move Right
            button_latch[right] = True
            test_block = active_block.move_Right()
        
        if not isCollision(game_map,test_block):
            active_block = test_block
        
        if ( buttons[down]  and not button_latch[down] ) or autodown_count >= 20:    #Move Down
            button_latch[down] = True if buttons[down] else False
            test_block = active_block.move_Down()
            if not isCollision(game_map,test_block):
                active_block = test_block
            else:
                game_map = game_map.set(active_block)
                clear_lines = game_map.checkLines()
                active_block = copy.deepcopy(next_block)
                next_block = Block()
                if isCollision(game_map,active_block):
                    globals.game_play = False
            autodown_count = 0
        else:
            autodown_count += sum(lines)/10 + 1
        
        if clear_lines > 0:
            if clear_count >=10:
                for row in range(21):
                    if game_map.map[row][1] == '=':
                        game_map.map.pop(row)
                        game_map.map.insert(0,['>','.','.','.','.','.','.','.','.','.','.','<'])
                        lines[clear_lines-1] += 1
                clear_count = 0
            else:
                clear_count += sum(lines)/20 + 1
        print("Held Block:")
        globals.held_block = held_block
        globals.held_block.print_Block()
        globals.game_map = game_map.set(active_block)
        globals.game_map.print_Map()
        print("Next Block:")
        globals.next_block = next_block
        globals.next_block.print_Block()
        for i in range(4):
            print("Lines "+str(i+1)+": "+str(lines[i]))
        print()
#end def tick