#Main file for managing the execution of state machines

import globals
import time

import menu

class Task:
    state = None
    period = None
    elapsed_time = None
    tick_fucntion = None
    
    def __init__(self):
        self.state = 0
        self.period = 0
        self.elapsed_time = 0
        self.tick_fucntion = None
#end def Task

def gcd(a, b):
    while(1):
        c = a%b
        if(c==0):
            return b
        a=b
        b=c
    return 0 #Not Taken
#end def gcd

task_menu = Task()
task_menu.tick_fucntion = lambda n : menu.tick(n)

tasks = [task_menu]  

def init_tasks():
    period_menu = 0.5 #test value
    
    period_main = period_menu
   #period_main = gcd(period_main, ...)
    
    i = 0
    tasks[i].state = 0
    tasks[i].period = period_menu/period_main
    tasks[i].elapsed_time = tasks[i].period
    tasks[i].tick_fucntion = lambda n : menu.tick(n)
   #i++
   #...
    
    globals.period_main = period_main
#end def init_tasks

def main():
    init_tasks()
    
    n = 0 #test value
    while n < 10:
        n += 1
            
        for task in tasks:
            task.elapsed_time += 1
            
            if task.elapsed_time >= task.period:
                task.elapsed_time = 0
                task.state = task.tick_fucntion(task.state)
        
        print(globals.test)       
        time.sleep(globals.period_main)

    print("main done")
main()
