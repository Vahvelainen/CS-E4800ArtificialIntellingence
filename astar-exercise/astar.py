from queue import PriorityQueue
from math import inf
from state import *

def astar(start_state, goaltest, h):

    """
    Perform A-star search.

    Finds a sequence of actions from `start_state` to some end state satisfying 
    the `goaltest` function by performing A-star search.

    This function returns a policy, i.e. a sequence of actions which, if
    successively applied to `start_state` will transform it into a state which
    satisfies `goaltest`.

    Parameters
    ----------
    start_state : State
       State object with `successors` function.
    goaltest : Function (State -> bool)
       A function which takes a State object as parameter and returns True if 
       the state is an acceptable goal state.
    h : Function (State -> float)
       Heuristic function estimating the distance from a state to the goal.
       This is the h(s) in f(s) = h(s) + g(s).
    
    Returns
    -------
    list of actions
       The policy for transforming start_state into one which is accepted by
       `goaltest`.
    """
    # Dictionary to look up predecessor states and the
    # the actions which took us there. It is empty to start with.
    predecessor = {} 
    # Dictionary holding the (yet) best found distance to a state,
    # the function g(s) in the formula f(s) = h(s) + g(s).
    g = {}
    # Priority queue holding states to check, the priority of each state is
    # f(s).
    # Elements are encoded as pairs of (prio, state),
    # e.g. Q.put( (prio, state ))
    # And gotten as (prio,state) = Q.get()
    Q = PriorityQueue()
    
    # TASK
    # ---------------------------------
    # Complete the A* star implementation.
    # Some variables have already been declared above (others may be needed
    # depending on your implementation).
    # Remember to return the plan (list of Actions).
    #
    # You can look at bfs.py to see how a compatible BFS algorithm can be
    # implemented.
    #
    # The A* algorithm can be found in the MyCourses material.
    #
    # Take care that you don't implement the GBFS algorithm by mistake:
    #  note that you should return a solution only when you *know* it is
    #  optimal (how?)
    #
    # Good luck!

    #successors of a state can be found with state.successors()
    print(type(start_state.successors())) #list
    print(type(start_state.successors()[0])) #of tuples
    print(start_state.successors()[0]) #(Action, MAPPGridState)
    #    (
    #    Action(source=((0, 0), (1, 1), (0, 1), (1, 0)), target=((0, 0), (1, 1), (0, 1), (1, 0)), cost=0),
    #    MAPPGridState(agents=((0, 0), (1, 1), (0, 1), (1, 0)), walls=frozenset(), nrows=5, ncols=5)
    #    )
    #action object have .source, .target & .cost variables
    #states have .agents (???), walls (???), .nrows & .ncols -- any of whichs should not be concerns
    ( act, stat ) = start_state.successors()[0]
    print(act.source)
    

    #prio function needs to be written
    Q.put( (2, stat ) )
    Q.put( (1, start_state ) )

    print('Q.get #1')
    print( Q.get() ) #Lets assume this pops the one with lowest prio, myth confirmed
    print('Q.get #2')
    print( Q.get() ) #freezes the program when nothing in queue

    # // The set of discovered nodes that may need to be (re-)expanded.
    # // Initially, only the start node is known.
    # // This is usually implemented as a min-heap or priority queue rather than a hash-set.
    # openSet := {start} 
    'openSet == Q'

    # // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # // to n currently known.
    # cameFrom := an empty map
    'cameFrom == predecessor' #is it a single object only? no its a map for all of them

    # // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    # gScore := map with default value of Infinity
    # gScore[start] := 0
    'gScore == g'

    # // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # // how cheap a path could be from start to finish if it goes through n.
    # fScore := map with default value of Infinity
    # fScore[start] := h(start)
    f = {}
    'fScore == f'

    'before starting, need to add starting state to priotity ques and give it g of its own cost'
    'maybe also f'


    # while openSet is not empty
    while not Q.empty():
    #     // This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
    #     current := the node in openSet having the lowest fScore[] value
        current = Q.get()
    #     if current = goal
    #         return reconstruct_path(cameFrom, current)
        if goaltest( current ):
            return [] #need  to implement reconstruct path

    #     openSet.Remove(current) 
        'happens automatically bc priorityque'
    #     for each neighbor of current
        for action, neigbor in current.successors():
    #         // d(current,neighbor) is the weight of the edge from current to neighbor
    #         // tentative_gScore is the distance from start to the neighbor through current
    #         tentative_gScore := gScore[current] + d(current, neighbor)
            'action cost is the distance in this situation'
            tempG = g[current] + action.cost
    #         if tentative_gScore < gScore[neighbor]
    #             // This path to neighbor is better than any previous one. Record it!
    #             cameFrom[neighbor] := current
    #             gScore[neighbor] := tentative_gScore
    #             fScore[neighbor] := tentative_gScore + h(neighbor)
            'this solution plays with the assumption that only better solutions are added to the priority que and not all of them'
    #             if neighbor not in openSet
    #                 openSet.add(neighbor)

    # // Open set is empty but goal was never reached
    # return failure



if __name__ == "__main__":
    # A few basic examples/tests.
    # Use test_astar.py for more proper testing.
    from mappgridstate import MAPPGridState
    from mappdistance import MAPPDistanceMax, MAPPDistanceSum
    import time
    #------------------------------------------------
    # Example 1
    grid_S = MAPPGridState([(0,0),(1,1),(0,1),(1,0)],nrows=5,ncols=5,walls=[])
    grid_G = MAPPGridState([(3,3),(2,2),(2,3),(3,2)],nrows=5,ncols=5,walls=[])
    print(
f"""
---------------------------------------------
Example 1
---------
Astar search with sum heuristic.
Start state:
{grid_S}
Goal state:
{grid_G}
Reference cost: optimal cost is 16.0
Runtime estimate: < 10 seconds""")
    
    stime = time.process_time()
    plan = list(astar(grid_S,
                      lambda state: state == grid_G, 
                      MAPPDistanceSum(grid_G)))
    etime = time.process_time()
    print(f"Plan:")
    s = grid_S
    print(s)
    for i,p in enumerate(plan):
        s = s.apply(p)
        print(f"step: {i}, cost: {p.cost}")
        print(str(s))
    print(f"Time: {etime-stime}")
    print(f"Calculated cost: {sum(p.cost for p in plan)}")
 
    #------------------------------------------------
    # Example 2
    grid_S = MAPPGridState.create_from_string(
        ["...#.........",
         "...#.........",
         "...#.........",
         "...########..",
         "..12......34.",
         "...###..###..",
         "...######....",
         "........#....",
         "........#...."])
        
    grid_G = MAPPGridState.create_from_string(
        ["...#.........",
         "...#.........",
         "...#.........",
         "...########..",
         "..34......21.",
         "...###..###..",
         "...######....",
         "........#....",
         "........#...."])

    print(
f"""
---------------------------------------------
Example 2
---------
Astar search, four agents and walls. Sum heuristic.
Start state:
{grid_S}
Goal state:
{grid_G}
Reference cost: optimal cost is 36.0
Runtime estimate: < 15 seconds""")
    
    stime = time.process_time()
    plan = list(astar(grid_S,
                      lambda state: state == grid_G, 
                      MAPPDistanceSum(grid_G)))
    etime = time.process_time()
    print(f"Plan:")
    s = grid_S
    print(s)
    for i,p in enumerate(plan):
        s = s.apply(p)
        print(f"step: {i}, cost: {p.cost}")
        print(str(s))

    print(f"Time: {etime-stime}")
    print(f"Calculated cost: {sum(p.cost for p in plan)}")
 
    #------------------------------------------------
    # Example 3
    grid_S = MAPPGridState([(0,0),(1,1),(0,1),(1,0)],nrows=5,ncols=5,walls=[])
    grid_G = MAPPGridState([(3,3),(2,2),(2,3),(3,2)],nrows=5,ncols=5,walls=[])
    print(
f"""
---------------------------------------------
Example 3
---------
Astar search, same as Example 1, but using the worse max heuristic.
Start state:
{grid_S}
Goal state:
{grid_G}
Reference cost: optimal cost is 16.0
Runtime estimate: < 5 minutes""")
    
    stime = time.process_time()
    plan = list(astar(grid_S,
                      lambda state: state == grid_G, 
                      MAPPDistanceMax(grid_G)))
    etime = time.process_time()
    print(f"Plan:")
    s = grid_S
    print(s)
    for i,p in enumerate(plan):
        s = s.apply(p)
        print(f"step: {i}, cost: {p.cost}")
        print(str(s))

    print(f"Time: {etime-stime}")
    print(f"Calculated cost: {sum(p.cost for p in plan)}")
 

