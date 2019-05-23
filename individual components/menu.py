#State Machine for Main Menu selection screen options
import globals
import screen
import client_bluetooth
import server_bluetooth

from enum import Enum

States = Enum('States', 'init GAME_SELECT_1P GAME_SELECT_2P GAME_1P GAME_SELECT_HOST GAME_SELECT_CONNECT GAME_2P GAME_OVER')
state = States.init

def tick():
    global state
    buttons = globals.buttons
    #Transitions
    if state == States.init:
        #print("--> 1P Game")
        state = States.GAME_SELECT_1P
        
    elif state == States.GAME_SELECT_1P:
        if buttons["A"]:
            #print("Starting 1P Game...")
            #globals.speaker_play = True
            globals.game_play = True
            state = States.GAME_1P
        elif buttons["Down"]:
            screen.MoveMenuArrowDown()
            #print("--> 2P Game")
            state = States.GAME_SELECT_2P
        else:
            state = States.GAME_SELECT_1P
            
    elif state == States.GAME_1P:
        if globals.game_play == True:           
            state = States.GAME_1P
        else:
            #print("Game Over")
            total = globals.lines[0]*1 + globals.lines[1]*3 + globals.lines[2]*5 + globals.lines[3]*8
            print("Score:")
            print("1-lines: "+str(globals.lines[0])+" *1 =\t"+str(globals.lines[0]*1))
            print("2-lines: "+str(globals.lines[1])+" *3 =\t"+str(globals.lines[1]*3))
            print("3-lines: "+str(globals.lines[2])+" *5 =\t"+str(globals.lines[2]*5))
            print("4-lines: "+str(globals.lines[3])+" *8 =\t"+str(globals.lines[3]*8))
            print("Total:\t"+str(total))
            #print("--> 1P Game")
            globals.output_menu = True
            state = States.GAME_OVER
            
        
    elif state ==  States.GAME_SELECT_2P:
        if buttons["A"]:
            #print("  --> Host Game")
            state = States.GAME_SELECT_HOST
        elif buttons["Up"]:
            screen.MoveMenuArrowUp()
            #print("--> 1P Game")
            state = States.GAME_SELECT_1P
        else:
            state = States.GAME_SELECT_2P
            
    elif state == States.GAME_SELECT_HOST:
        if buttons["A"]:
            #print("  --> Hosting Game...")
            #globals.speaker_play = True
            globals.game_play = True
            state = States.GAME_2P
        elif buttons["B"]:
            #print("--> 2P Game")
            state = States.GAME_SELECT_2P
        elif buttons["Down"]:
            #print("  --> Connect to a Game")
            state = States.GAME_SELECT_CONNECT
        else:
            state = States.GAME_SELECT_HOST
            
    elif state == States.GAME_SELECT_CONNECT:
        if buttons["A"]:
            print("  --> Connecting to Game...")
            #globals.speaker_play = True
            globals.game_play = True
            state = States.GAME_2P
        elif buttons["B"]:
            #print("--> 2P Game")
            state = States.GAME_SELECT_2P
        elif buttons["Up"]:
            #print("  --> Host Game")
            state = States.GAME_SELECT_HOST
        else:
            state = States.GAME_SELECT_CONNECT
            
    elif state == States.GAME_2P:
        if buttons["B"]:
            pass
            #globals.game_play = False
            #print("--> 2P Game")
            state = States.GAME_SELECT_2P
        else:
            state = States.GAME_2P
    
    elif state == States.GAME_OVER:
        if buttons["B"]:
            state = States.GAME_SELECT_1P
        else:
            state = States.GAME_OVER
    else:
        state = States.init
    
    #Actions
    if state == States.init:
        pass
    elif state == States.GAME_SELECT_1P:
        pass
    elif state == States.GAME_1P:
        pass
    elif state == States.GAME_SELECT_2P:
        pass
    elif state == States.GAME_SELECT_HOST:
        pass
    elif state == States.GAME_SELECT_CONNECT:
        pass
    elif state == States.GAME_2P:
        pass
    elif state == States.GAME_OVER:
        pass
        
#end def tick
