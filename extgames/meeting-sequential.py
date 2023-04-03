
from extgames import reduceToNormalFormGame, ChanceMove, Move, Terminal

# Meeting in the same location

MEETINGSEQ = Move(0,[("0Location1",Move(1,[("1Location1",Terminal([1,1])),("1Location2",Terminal([0,0]))])),
                    ("0Location2",Move(1,[("1Location1",Terminal([0,0])),("1Location2",Terminal([1,1]))]))])
MEETINGSEQ_OBS_0 = []
MEETINGSEQ_OBS_1 = ["0Location1","0Location2"]
MEETINGSEQ_OBS = dict()
MEETINGSEQ_OBS[0] = MEETINGSEQ_OBS_0
MEETINGSEQ_OBS[1] = MEETINGSEQ_OBS_1

reduceToNormalFormGame(MEETINGSEQ,MEETINGSEQ_OBS)
