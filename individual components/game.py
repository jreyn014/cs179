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
    
    def printM(self):
        M = self.block
        n = self.n
        for i in range(0,n):
            print(M[i])
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

def tick():
    global state
    global game_map
    global active_block
    
    #Transitions
    if state == States.init:
        state = States.GAME_OFF
        
    elif state == States.GAME_OFF:
        if globals.game_play == True:
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
        if buttons[A]:
            test_block = active_block.rotate_ACW()
        elif buttons[B]:
            test_block = active_block.rotate_CW()
        if buttons[left] and not buttons[right]:
            test_block = active_block.move_Left()
        elif buttons[right] and not buttons[left]:
            test_block = active_block.move_Right()
        if buttons[down]:
            test_block = active_block.move_Down()
        if not isCollision(game_map,test_block):
            active_block = test_block
        new_map = game_map.set(active_block)
        new_map.print_Map()
#end def tick