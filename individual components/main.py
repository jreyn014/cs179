#Main file for managing the execution of state machines

import globals
import time
import threading

import menu
import speaker
import buttons
import game
import screen

class Task:    
    def __init__(self, tick, period):
        self.tick = tick            # State Machine object
        self.period = period        # in milliseconds
        self.elapsed = period
#end def Task

# Task(SM, milliseconds)
task_buttons = Task(buttons.tick,50)
task_menu = Task(menu.tick,100)
task_speaker = Task(speaker.tick,10)
task_game = Task(game.tick,50)
#task_screen = Task(screen.tick, 500)

tasks = [ task_buttons, task_menu, task_speaker, task_game ]
#tasks = [ task_buttons, task_menu, task_speaker, task_game, task_screen ]

def gcd(x, y):
    while y:
        x, y = y, x%y
    return x 
#end def gcd

def main_tick(period_main):
    for task in tasks:
        task.elapsed += period_main
        
        if task.elapsed >= task.period:
            task.tick()
            task.elapsed = 0
#end def main_tick

def main():
    screen.InitDisplay()
    
    period_main = tasks[0].period
    for task in tasks:
        period_main = gcd(period_main, task.period)
    
    screen.SetupGameScreen()
    
    while True:
        screen.MainGame()
        screen.NextBlock()
        screen.HeldBlock()
        threading.Thread(target=main_tick,args=[period_main]).start()
        time.sleep(period_main/1000)
    
    return 0
main()
