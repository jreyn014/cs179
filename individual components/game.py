import random

Blocks = {
'I' : [
[0,0,0,0],
[1,1,1,1],
[0,0,0,0],
[0,0,0,0]
],

'O' : [
[0,0,0,0],
[0,1,1,0],
[0,1,1,0],
[0,0,0,0]
],

'J' : [
[0,0,0],
[1,1,1],
[0,0,1],
],

'L' : [
[0,0,0],
[1,1,1],
[1,0,0],
],

'S' : [
[0,0,0],
[0,1,1],
[1,1,0]
],

'Z' : [
[0,0,0],
[1,1,0],
[0,1,1]
],

'T' : [
[0,0,0],
[1,1,1],
[0,1,0]
]
}

class Block:
    def __init__(self, b):
        self.block = b
        self.n = len(b[0])
    
    def rotate_CW(self):
        M = self.block
        n = self.n
        for x in range(0, (int(n/2))):
            for y in range(x, n-x-1):
                T =  M[n-1-y][x]
                M[n-1-y][x] = M[n-1-x][n-1-y]
                M[n-1-x][n-1-y] = M[y][n-1-x]
                M[y][n-1-x] = M[x][y]
                M[x][y] = T
    #end def
    
    def rotate_ACW(self):
        M = self.block
        n = self.n
        for x in range(0, (int(n/2))):
            for y in range(x, n-x-1):
                T = M[x][y]
                M[x][y] = M[y][n-1-x]
                M[y][n-1-x] = M[n-1-x][n-1-y]
                M[n-1-x][n-1-y] = M[n-1-y][x]
                M[n-1-y][x] = T
    #end def
    
    def printM(self):
        M = self.block
        n = self.n
        for i in range(0,n):
            print(M[i])
        print()
#end class Block

def game_SM(state):
    
    #Transitions
    if state == 0: #init
        x = range(10)
        y = range(20)
        game_map = [x,y]
        
        state = 1
    elif state == 1: 
        state = 1
    #elif state == 2: 
    
    else:
        state = 0
    
    #Actions
    if state == 0:
        x = range(10)
        y = range(20)
        game_map = [x,y]
    elif state == 1:
        x = range(10)
    #elif state == 2:
        
    return state

game_state = 0
#while True:
#    time.sleep(0.01)
#    game_state = game_SM(game_state)

x = 10
y = 20
game_map = [ [0] * x ] * y

print()
for row in reversed(range(y)):
    print(">", end = ' ')
    for col in game_map[row]:
        print(str(col), end=' ')
    print("<")

print(" ",end=' ')    
for i in range(x):
    print("^", end = ' ')
print(" ")



test = Block(Blocks['I'])
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()

test = Block(Blocks['O'])
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()
test.printM()
test.rotate_ACW()

test = Block(Blocks['J'])
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()

test = Block(Blocks['L'])
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()

test = Block(Blocks['S'])
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()

test = Block(Blocks['Z'])
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()

test = Block(Blocks['T'])
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
test.printM()
test.rotate_CW()
