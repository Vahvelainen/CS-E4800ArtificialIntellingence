
#
# Construct PDB heuristics for N-Puzzle

import Npuzzle

import queue

# Breadth-First Search (uninformed)
#
# Modify the breadth-first search algorithm to record the distances of
# all state from the initial state, and to return those distances.
# It is best to use a dictionary, so that distances of state can be
# recorded as distances[s] = ... and accessed as distances[s].

def breadthFirstSearch(initialstate):
    visited = dict() # dictionary (hash table) for holding visited states
    #### YOUR CODE HERE ####
    distances = {}
        
    Q = queue.Queue(maxsize=0) # first-in-first-out queue

    Q.put( initialstate ) # Insert the initial state in the queue
    visited[initialstate] = 1 #this could be remvoed for the use of distances but eh
    distances[initialstate] = 0
    
    while not Q.empty():
        state = Q.get() # Next un-expanded state from the queue
        for aname,s,cost in state.successors(): # Go through all successors of state
            if s not in visited: # Was the state visited already?
                visited[s] = 1
                #### YOUR CODE HERE ####
                distances[s] = distances[state] + 1
                Q.put( s )
    #### YOUR CODE HERE ####
    return distances #return like a dictionary?

# Construct a PDB heuristic based on a subset of tiles
#
# makePDBheuristics takes as input
#
# - the goal state to which distance is estimated
# - the set of tiles that are to be included in the PDB
#
# makePDBheuristics returns a function that
#
# - takes a state as input
# - returns a lower bound estimate for the distance to the goal state

def makePDBheuristic(goalState,tiles):
    #### YOUR CODE HERE ####
    abstractGoal = goalState.abstract(tiles)
    distances = breadthFirstSearch(abstractGoal)
    def heuristic(state):
        abstractState = state.abstract(tiles)
        # print('goalstate:')
        # print(str(goalState))
        # print('tiles:')
        # print(tiles)
        # print('state:')
        # print(state)
        # print('Abstract of the goal state:')
        # print(abstractState)
        # print('Abstract of the state:')
        # print(abstractState)
        # print('Lower bound distance to goal')
        # print(distances[abstractState])
        # print('Runnin output of makePDBheuristic')
        # input('press enter to continue')
        return distances[abstractState]
    return heuristic

# Construct a PDB heuristics based on PDBs for two subsets of tiles
#
# This is like makePDBheuristics, except that two PDBs are constructed
# and used for deriving a lower bound distance estimate.
# Depending on whether the subsets intersect or not, the lower bounds
# from the two PDBs can be combined either by summing or by maximizing.
#
# makePDBheuristic2 return one function just like makePDBheuristic2 does.

def makePDBheuristic2(goalState,tiles1,tiles2):
    #### YOUR CODE HERE ####
    h1 = makePDBheuristic(goalState,tiles1)
    h2 = makePDBheuristic(goalState,tiles2)
    def intersectingHeuristic(state):
        return max( h1(state), h2(state) )
    def nonIntersectingHeuristic(state):
        return h1(state) + h2(state)
    #If any tiles of the first set are in the second
    if any( tile in tiles2 for tile in tiles1 ):
        return intersectingHeuristic
    else:
        return nonIntersectingHeuristic
