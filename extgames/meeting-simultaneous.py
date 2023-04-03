
from extgames import reduceToNormalFormGame, ChanceMove, Move, Terminal

# Meeting in the same location

MEETING = Move(0,[("0Location1",Move(1,[("1Location1",Terminal([1,1])),("1Location2",Terminal([0,0]))])),
                    ("0Location2",Move(1,[("1Location1",Terminal([0,0])),("1Location2",Terminal([1,1]))]))])
MEETING_OBS_0 = []
MEETING_OBS_1 = []
MEETING_OBS = dict()
MEETING_OBS[0] = MEETING_OBS_0
MEETING_OBS[1] = MEETING_OBS_1

reduceToNormalFormGame(MEETING,MEETING_OBS)
