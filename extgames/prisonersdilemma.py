
from extgames import reduceToNormalFormGame, ChanceMove, Move, Terminal

# Prisoner's dilemma

PRISONERS = Move(0,[
                    ( "0ShutUp", Move( 1, [ ("1ShutUp",Terminal([-1,-1])), ("1Cooperate",Terminal([-3,0])) ]) ),
                    ( "0Cooperate", Move( 1, [ ("1ShutUp",Terminal([0,-3])),("1Cooperate",Terminal([-2,-2])) ]) )
                    ]
                )
PRISONERS_OBS_0 = []
PRISONERS_OBS_1 = []
PRISONERS_OBS = dict()
PRISONERS_OBS[0] = PRISONERS_OBS_0
PRISONERS_OBS[1] = PRISONERS_OBS_1

reduceToNormalFormGame(PRISONERS,PRISONERS_OBS)
