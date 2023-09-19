
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

POKER = ChanceMove([
                  ( 0.5, "RHIGH", Move( 0, [
                          ("0BET", Move( 1, [
                                  ("1CALL",Terminal([ 2, -2 ])), # 2, -2 both bet the 2 but player0 tkes the win
                                  ("1FOLD",Terminal([ 1, -1 ])), # 1, -1 same but player1 doesnt call -> 1 less bet on stake
                              ])),
                          ("0FOLD", Terminal([ -1, 1 ])), # Player0 is a dum dum and gives win to player 2
                    ])),
                  ( 0.5, "RLOW", Move( 0, [
                          ("0BET", Move( 1, [
                                  ("1CALL",Terminal([ -2, 2 ])), #Player1 sees trough the bluff and gets the maximum stake
                                  ("1FOLD",Terminal([ 1, -1 ])), #Player1 plays it safe and loses the original bet
                              ])),
                          ("0FOLD", Terminal([-1, 1])), # Player0 isnt trying anything, just going to the next game
                    ])),
                ]) 
POKER_OBS_0 = ["RHIGH","RLOW"]
POKER_OBS_1 = ["0BET","0FOLD"]
POKER_OBS = dict()
POKER_OBS[0] = POKER_OBS_0
POKER_OBS[1] = POKER_OBS_1

reduceToNormalFormGame(POKER,POKER_OBS)

# Probabilities: does this use bayesian rule or what? Nash equilibrium

# bluff: player0 strategy0 ( p )
# p = 1q + 2q
# 
# don't bluff: player0 strategy1 ( 1 - p )
# 1 - p = 1.5q + 1q
#
# call: player1 strategy0 ( q )
# q = 1p + 0.5p
#
# fold: player1 strategy1
# 1 - q = 0p + 1p
#
# suppose p = 0.75
#
#
# q = 