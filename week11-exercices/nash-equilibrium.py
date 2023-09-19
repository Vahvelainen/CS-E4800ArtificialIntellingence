import nashpy as nash
import nashpy as nash
import numpy as np

# Normal form game
row_player = [
  #a
    [ 1, 9, 7 ],
  #b
    [ 3, 5, 4 ],
  #c
    [ 2, 5, 8 ],
]

colum_player = [
  #d
    [ 5, 2, 9 ],
  #f
    [ 1, 0, 0 ],
  #g
    [ 2, 0, 1 ],
]

def iteratedStrictDominance(row_player, colum_player):
  #How do you keep the indexes
  indexes = [
    list(range(len(row_player))),
    list(range(len(colum_player)))
  ]
  improving = True
  while improving:
    improving = False
    #Switch between agents
    for axis, agent in enumerate([row_player, colum_player]):
      for i, strat1 in enumerate(agent):
        is_dominated = False
        for strat2 in agent:
          #Check if dominated
          if sum(strat1) < sum(strat2):
              print ( str(indexes[axis][i]) + ' removed from ' + str(axis))
              # the axis dont get deleted propely in between
              print( agent )
              is_dominated = True
              row_player = np.delete(row_player, i, axis)
              colum_player = np.delete(colum_player, i, 1 - axis)
              del indexes[axis][i]
              break
        if is_dominated:
          improving = True
          break
  return indexes

ins = iteratedStrictDominance(row_player, colum_player)
print(ins)

# rps = nash.Game(row_player, colum_player)
# print(rps)

# eqs = rps.support_enumeration()
# print(list(eqs))

# iterations = 100
# np.random.seed(0)
# play_counts = rps.fictitious_play(iterations=iterations)
# for row_play_count, column_play_count in play_counts:
#     print(row_play_count, column_play_count)
