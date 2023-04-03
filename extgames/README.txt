
This archive contains the following files

  extgames.py  Representation of games in extensive form, translation to normal form
  bachstravinsky.py        Example
  meeting-sequential.py    Example
  meeting-simultaneous.py  Example
  prisonersdilemma.py      Example
  template-poker.py        Template for the solution of the exercise

Before proceeding with the exercise, try the examples by e.g. writing

  python3 bachstravinsky.py

The program then outputs information about the different strategies
of the game, the pay-off vectors of the different strategy profiles,
the strictly dominated strategies, and finally the corresponding
normal form game.

The classes to represent extensive form games are described in extgames.py.

A difference between the representation used in this exercise and the
representation in the written course material is in the representation
of imperfect information.
In the written material, the observational indistinguishability of
two nodes in an extensive form game is indicated by a dashed line
drawn between the nodes.
In this exercise, imperfect information is represented differently.
For every extensive form game, we indicate which _moves/actions_
can be observed by each player. Two nodes in an extensive form game
can be distinguished by a player if the sequences of observable moves
from the root to that node are different. For example, in the simple Poker
game in the course material, the first player can distinguish between
the chance move of randomly making the card High or Low (with move
names RHIGH and RLOW in the solution template). The second player
cannot make this distinction, so the second player does not know,
what the card is, and which subgame is being played. What the second
player can observe is the 0BET and 0FOLD actions of the player 0.

Your task in this exercise is to complete the formalization of the simple
Poker game. What you need to do is the following.

1. Copy template-poker.py to poker.py.
2. Formalize the game tree for the extensive game, with help by looking
   at the example files.
3. The representation of imperfect information is already completed, so
   there is no need to touch the POKER_OBS variables at all.
4. Test your solution by writing

      python3 poker.py

   and see that the output makes sense (the strategies, the values of
   all of the strategy profiles, and the strictly dominated strategies).
5. Submit your solution on the course's A+ pages.
