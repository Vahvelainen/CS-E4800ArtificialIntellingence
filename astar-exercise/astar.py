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
    predecessor = {} #states
    cameFrom = {} #actionn

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
    # it returns a list of tuples with ( Action, State )
    # ( action, state ) = start_state.successors()[0]
    #action object have .source, .target & .cost variables -- source and target are not types of State
    #states have .agents (???), walls (???), .nrows & .ncols -- any of whichs should not be concerns
    #action.source and action.target might be comparable to state.agents but eh...

    best = float('inf')
    goalState = None


    #Put starting state to the Queue with 0 prio
    Q.put( (0, start_state) )
    #Give the start sate a g 0 incase we test it
    g[start_state] = 0

    # while openSet is not empty
    while not Q.empty():
        #Pop the state with lowest f (it gets deleted from the queue)
        currentPrio, current = Q.get()

        #Check if in the goal
        if currentPrio >= best:
            return reconstructPath(goalState, predecessor, cameFrom)

        #Add neighbor states to the Q
        for action, neighbor in current.successors():
            #should propabl do some if here to not loop around
            #only do this if the g
            neighbor_g = g[current] + action.cost

            if goaltest(neighbor) and neighbor_g < best:
                best = neighbor_g
                goalState = neighbor

            if not neighbor in g.keys(): # or neighbor_g < best:
                #the action needs to be saved for the path reconstruction
                predecessor[neighbor] = current
                cameFrom[neighbor] = action
                g[neighbor] = neighbor_g
                f_score = neighbor_g + h(neighbor)
                Q.put( (f_score, neighbor) )

    # // Open set is empty but goal was never reached
    return []

def reconstructPath(goalState, predecessor, cameFrom):
    #action object have .source, .target & .cost variables
    actionList = []
    nextState = goalState
    while nextState in predecessor.keys():
        actionList.insert(0, cameFrom[nextState] )
        nextState = predecessor[nextState]
    return actionList

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
 

