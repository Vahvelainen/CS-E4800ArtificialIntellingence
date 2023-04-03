
from extgames import reduceToNormalFormGame, ChanceMove, Move, Terminal

# Bach or Stravinsky with non-simultaneous moves

BS = Move(0,[("0Bach",Move(1,[("1Bach",Terminal([2,1])),("1Stravinsky",Terminal([0,0]))])),
             ("0Stravinsky",Move(1,[("1Bach",Terminal([0,0])),("1Stravinsky",Terminal([1,2]))]))])
BS_OBS_0 = []
BS_OBS_1 = [] # ["0Bach","0Stravinsky"] # For a game in which non-zero pay-offs can be avoided!
BS_OBS = dict()
BS_OBS[0] = BS_OBS_0
BS_OBS[1] = BS_OBS_1

reduceToNormalFormGame(BS,BS_OBS)
