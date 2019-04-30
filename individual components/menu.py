#State Machine for Main Menu selection screen options

import globals

class Menu():
    def __init__(self):
        self.state = 0
        
    def tick(self):
        state = self.state
        
        if(globals.test < 25):
            globals.test += 1
            print("Menu: "+str(globals.test))
        
        self.state = state
#end class Menu
