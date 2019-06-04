#State Machine for Main Menu selection screen options
import globals
import screen
import combined_btooth as bt

from enum import Enum

States = Enum('States', 'init GAME_SELECT_1P GAME_SELECT_2P GAME_1P GAME_SELECT_HOST GAME_SELECT_CONNECT GAME_2P GAME_OVER')
state = States.init

def tick():
    global state
    buttons = globals.buttons
    #Transitions
    if state == States.init:
        state = States.GAME_SELECT_1P
        
    elif state == States.GAME_SELECT_1P:
        if buttons["A"]:
            globals.game_play = True
            state = States.GAME_1P
        elif buttons["Down"]:
            screen.MoveMenuArrowDown()
            state = States.GAME_SELECT_2P
        else:
            state = States.GAME_SELECT_1P
            
    elif state == States.GAME_1P:
        if globals.game_play == True:           
            state = States.GAME_1P
        else:
            total = globals.lines[0]*1 + globals.lines[1]*3 + globals.lines[2]*5 + globals.lines[3]*8
            print("Score:")
            print("1-lines: "+str(globals.lines[0])+" *1 =\t"+str(globals.lines[0]*1))
            print("2-lines: "+str(globals.lines[1])+" *3 =\t"+str(globals.lines[1]*3))
            print("3-lines: "+str(globals.lines[2])+" *5 =\t"+str(globals.lines[2]*5))
            print("4-lines: "+str(globals.lines[3])+" *8 =\t"+str(globals.lines[3]*8))
            print("Total:\t"+str(total))
            globals.output_game_over = True
            state = States.GAME_OVER
            
        
    elif state ==  States.GAME_SELECT_2P:
        if buttons["A"]:
            globals.output_hold_menu = True
            state = States.GAME_SELECT_HOST
        elif buttons["Up"]:
            screen.MoveMenuArrowUp()
            state = States.GAME_SELECT_1P
        else:
            state = States.GAME_SELECT_2P
            
    elif state == States.GAME_SELECT_HOST:
        if buttons["A"]:
            if(globals.isMultiplayer == False):
                globals.isMultiplayer = True
                globals.output_connecting = True
                bt.findHostMAC()
                globals.client, globals.recv_thread = bt.WaitForClient()
                globals.game_play = True
                state = States.GAME_2P
            else:
                States.GAME_SELECT_HOST
        elif buttons["B"]:
            globals.output_menu = True
            state = States.GAME_SELECT_1P
        elif buttons["Down"]:
            screen.MoveMenuArrowDown()
            state = States.GAME_SELECT_CONNECT
        else:
            state = States.GAME_SELECT_HOST
            
    elif state == States.GAME_SELECT_CONNECT:
        if buttons["A"]:
            if(globals.isMultiplayer == False):
                globals.isMultiplayer = True
                globals.output_connecting = True
                found, globals.recv_thread = bt.FindHost()
                if(found):
                    globals.game_play = True
                    state = States.GAME_2P
                else:
                    globals.isMultiplayer - False
                    globals.output_menu = True
                    state = States.GAME_SELECT_1P
            else:
                state = States.GAME_SELECT_CONNECT
        elif buttons["B"]:
            globals.output_menu = True
            state = States.GAME_SELECT_1P
        elif buttons["Up"]:
            screen.MoveMenuArrowUp()
            state = States.GAME_SELECT_HOST
        else:
            state = States.GAME_SELECT_CONNECT
            
    elif state == States.GAME_2P:
        if globals.game_play == True:           
            state = States.GAME_2P
        else:
            total = globals.lines[0]*1 + globals.lines[1]*3 + globals.lines[2]*5 + globals.lines[3]*8
            print("Score:")
            print("1-lines: "+str(globals.lines[0])+" *1 =\t"+str(globals.lines[0]*1))
            print("2-lines: "+str(globals.lines[1])+" *3 =\t"+str(globals.lines[1]*3))
            print("3-lines: "+str(globals.lines[2])+" *5 =\t"+str(globals.lines[2]*5))
            print("4-lines: "+str(globals.lines[3])+" *8 =\t"+str(globals.lines[3]*8))
            print("Total:\t"+str(total))
            globals.output_game_over_multiplayer = True
            globals.output_win = True
            bt.closeSocket()
            globals.recv_thread.join()
            
            globals.client = None
            globals.recv_thread = None
            globals.isMultiplayer = False
            state = States.GAME_OVER
    
    elif state == States.GAME_OVER:
        if buttons["B"]:
            globals.output_menu = True
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
