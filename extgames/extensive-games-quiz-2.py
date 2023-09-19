
from extgames import reduceToNormalFormGame, ChanceMove, Move, Terminal

# A simple Poker game with one card only

# Complete the stripped-down version of Poker (see the training exercise material for details!
# in the file template-poker.py, after copying it to poker.py.

# In this simplified
# version both players bet 1 unit of money, only one card is dealt to the first player, the first player bets one unit more money
# to stay in the game, or folds (exits the game, losing his initial bet to the second player), and then the second player either
# folds (losing his initial bet), or calls (by betting more money) to see if the card the first player holds has a high value. If it
# is, then the first player wins all money, and otherwise the second player wins

# Hint: Player 0 will have 4 strategies, and Player 1 will have two strategies.
# Two of the strategies of Player 0 will be automatically eliminated by the application of strict dominance (already implemented in extgames.py),
# so in the final result there will be two strategies for each player.
# Use the names RLOW and RHIGH for the two chance moves,
# 0BET and 0FOLD for the two actions of Player 0, and 1CALL and 1FOLD for the two actions of Player 1.

# This form is correct I think but the terminal valuews need to be reconsidered

#Player 0 folds and its high -> -1 for the bet, +1 for the other
#Player 0 Bets and its high -> 

EXTGAME = Move(0, [
    ('A', Move(1, [
      ('C', Terminal([ 2 , 1 ])), # 50% 0,2 & 50% 4,0 => 2,1
      ('D', Terminal([ 1 , 4 ])), # 80% 0,5 & 20% 5,0 => 1,4
    ])),
    ('B', Move(1, [
      ('C', Terminal([ 2 , 1 ])), # 33% 0,3 & 66% 3,0 => 2,1
      ('D', Terminal([ 3 , 3 ])), # 75% 3,4 & 25% 3,0 => 3,3
    ])),
])

EXTGAME_OBS_0 = []
EXTGAME_OBS_1 = []
EXTGAME_OBS = dict()
EXTGAME_OBS[0] = EXTGAME_OBS_0
EXTGAME_OBS[1] = EXTGAME_OBS_1

reduceToNormalFormGame(EXTGAME,EXTGAME_OBS)