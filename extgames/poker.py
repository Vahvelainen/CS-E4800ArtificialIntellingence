
from extgames import reduceToNormalFormGame, ChanceMove, Move, Terminal

# A simple Poker game with one card only

POKER = Terminal([0,0]) # THIS MUST BE REPLACED WITH THE EXTENSIVE FORM GAME BY YOU!
POKER_OBS_0 = ["RHIGH","RLOW"]
POKER_OBS_1 = ["0BET","0FOLD"]
POKER_OBS = dict()
POKER_OBS[0] = POKER_OBS_0
POKER_OBS[1] = POKER_OBS_1

reduceToNormalFormGame(POKER,POKER_OBS)
