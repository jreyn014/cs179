#State Machine for Main Menu selection screen options

import globals

class Menu():
    def __init__(self):
        self.state = 0
        
    def tick(self):
        state = self.state
        
        #Transitions
        if state == 0:
            state = 1
        elif state == 1:
            if globals.test < 9:
                state = 1
                globals.test += 1
            else:
                state = 2
        elif state == 2:
            state = 2
        else:
            state = 0
        
        #Actions
        if state == 0:
            pass
        elif state == 1:
            print("Menu: "+str(globals.test))
        elif state == 2:
            pass
        else:
            pass
            
        self.state = state
    #end def tick
#end class Menu
