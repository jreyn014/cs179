#import RPi.GPIO as GPIO
import globals

#Software PWM available on all pins
#Hardware PWM available on GPIO12, GPIO13, GPIO18, GPIO19
pwmPin = 32 #GPIO12, PWM0

notes = {
"C0" : -8, "C#0" : -7, "Db0" : -7, "D0" : -6, "D#0" : -5, "Eb0" : -5, "E0" : -4,
"F0" : -3, "F#0" : -2, "Gb0" : -2, "G0" : -1, "G#0" : 0, "Ab0" : 0, "A0" : 1, "A#0" : 2, "Bb0" : 2, "B0" : 3, 

"C1" : 4, "C#1" : 5, "Db1" : 5, "D1" : 6, "D#1" : 7, "Eb1" : 7, "E1" : 8, 
"F1" : 9,"F#1" : 10, "Gb1" : 10, "G1" : 11, "G#1" : 12, "Ab1" : 12, "A1" : 13, "A#1" : 14, "Bb1" : 14, "B1" : 15,

"C2" : 16, "C#2" : 17, "Db2" : 17, "D2" : 18, "D#2" : 19, "Eb2" : 19, "E2" : 20,
"F2" : 21, "F#2" : 22, "Gb2" : 22, "G2" : 23, "G#2" : 24, "Ab2" : 24, "A2" : 25, "A#2" : 26, "Bb2" : 26, "B2" : 27, 

"C3" : 28, "C#3" : 29, "Db3" : 29, "D3" : 30, "D#3" : 31, "Eb3" : 31, "E3" : 32,
"F3" : 33, "F#3" : 34, "Gb3" : 34, "G3" : 35, "G#3" : 36, "Ab3" : 36, "A3" : 37, "A#3" : 38, "Bb3" : 38, "B3" : 39,

"C4" : 40, "C#4" : 41, "Db4" : 41, "D4" : 42, "D#4" : 43, "Eb4" : 43, "E4" : 44,
"F4" : 45, "F#4" : 46, "Gb4" : 46, "G4" : 47, "G#4" : 48, "Ab4" : 48, "A4" : 49, "A#4" : 50, "Bb4" : 50, "B4" : 51,

"C5" : 52, "C#5" : 53, "Db5" : 53, "D5" : 54, "D#5" : 55, "Eb5" : 55, "E5" : 56,
"F5" : 57, "F#5" : 58, "Gb5" : 58, "G5" : 59, "G#5" : 60, "Ab5" : 60, "A5" : 61, "A#5" : 62, "Bb5" : 62, "B5" : 63,

"C6" : 64, "C#6" : 65, "Db6" : 65, "D6" : 66, "D#6" : 67, "Eb6" : 67, "E6" : 68,
"F6" : 69, "F#6" : 70, "Gb6" : 70, "G6" : 71, "G#6" : 72, "Ab6" : 72, "A6" : 73, "A#6" : 74, "Bb6" : 74, "B6" : 75,

"C7" : 76, "C#7" : 77, "Db7" : 77, "D7" : 78, "D#7" : 79, "Eb7" : 79, "E7" : 80,
"F7" : 81, "F#7" : 82, "Gb7" : 82, "G7" : 83, "G#7" : 84, "Ab7" : 84, "A7" : 85, "A#7" : 86, "Bb7" : 86, "B7" : 87,

"C8" : 88, "C#8" : 89, "Db8" : 89, "D8" : 90, "D#8" : 91, "Eb8" : 91, "E8" : 92,
"F8" : 93, "F#8" : 94, "Gb8" : 94, "G8" : 95, "G#8" : 96, "Ab8" : 96, "A8" : 97, "A#8" : 98, "Bb8" : 98, "B8" : 99,
}

def getFrequency(x):    
    return (2**((notes[x] - 49) / 12) * 440)

#Mock Music
test = [
"C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0", 
"C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1", 
"C2","C#2","D2","D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2", 
"C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3", 
"C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4", 
"C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5","B5", 
"C6","C#6","D6","D#6","E6","F6","F#6","G6","G#6","A6","A#6","B6",
"C7","C#7","D7","D#7","E7","F7","F#7","G7","G#7","A7","A#7","B7", 
"C8","C#8","D8","D#8","E8","F8","F#8","G8","G#8","A8","A#8","B8",
]


state = 0
index = 0
        
def tick():
    global state
    global index
    
    #Transitions
    if state == 0: #init
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(pwmPin, GPIO.OUT)
        index = 0
        globals.speaker_play = True
        #pwm = GPIO.PWM(pwmPin, 0)
        #pwm.stop()
        state = 1                   #GO: PWM_OFF
    
    elif state == 1: #PWM_OFF
        if(globals.speaker_play):        #TO: PWM_ON
            #pwm.ChangeFrequency(0)
            #pwm.start(50)
            index = 0
            state = 2
            globals.speaker_play = False
        else:                       #TO: PWM_ON
            state = 1   
            
    elif state == 2: #PWM_ON
        if(index >= len(test)-1):     #TO: PWM_OFF
            #pwm.stop()
            state = 1
        else:                       #TO: PWM_ON
            index += 1
            state = 2
    else:
        state = 0
    
    #Actions
    if state == 0:
        pass
        #pwm.stop()
    elif state == 1:        #PWM_OFF
        pass
        #pwm.stop()
    elif state == 2:        #PWM_ON
        note = test[index]
        freq = getFrequency(note)
        print("    "+note+": "+str(freq))
        #pwm.ChangeFrequency(freq)
    
#end def tick

#GPIO.cleanup()
