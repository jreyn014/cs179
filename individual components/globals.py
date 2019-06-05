#Store globals here
#Sort alphabetically

atk_in = 0

buttons = {
"A"     : False,
"B"     : False, 
"Up"    : False,
"Down"  : False, 
"Left"  : False, 
"Right" : False
}

client = None
flag = 1
game_map = None
game_map_old = None
game_play = False
hold_block = None
hold_block_old = None
isMultiplayer = False
lines = [0,0,0,0]
lines_old = [0,0,0,0]
next_block = None
next_block_old = None
output_connecting = False
output_game_over = False
output_game_over_multiplayer = False
output_hold_menu = False
output_menu = True
output_win = False
recv_thread = None
speaker_period = 0

test = 0
