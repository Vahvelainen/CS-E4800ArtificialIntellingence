
from logic import AND, OR, NOT, ATOM, IMPL, EQVI
from z3_wrapper import solve, Bool

# The function findPlan:
#   source     Formula that describes the source/initial initial states
#   transition Formula that describes the transition relation
#   target     Formula that describes the target/goal states
#   MAX        Last time point to be considered. Must be MAX>=0.
#
# The atomic formulas in each of these three inputs are pairs (s,i) where
#    s is a string
#    i is an integer 0 or 1
#
# For 'source' and 'target' i is always 0.
#
# Now each of these atomic formula names have to be turned to strings with
# the correct time tags. For example, ATOM( ("x",0) ) appearing
# in the 'target' formula has to be replaced by ATOM ("x@7") if
# the last time point in the state sequence being considered is 7.
# These replacements are done by the method 'map' that is provided
# for all formulas.
# Similarly, there must be several copies of the 'transition' formula,
# obtained by adding 0,1,2,...,T-1 to the time tags, where T is
# the last time point in the state sequence. This instantiations
# are done by the function 'instantiate' given below.

# For a given t, replace atom names (name,i) by name + "@" + str(i+t).

def instantiate(f,t):
    return f.map(lambda si : si[0] + "@" + str(si[1]+t))

# The main function for finding state/action sequences

# Find a state sequence from source to target, with every pair of
# consecutive intermediate states satisfying the transition relation.
# If no solutions are found, return None.
# If a solution is found, return (T,assignment), where 'T' is the last
# time point and 'assignment' is the assignment returned by Z3.

def findPlan(source,transition,target,MAX : int):
    # T is the last time point considered.
    for T in range(0,MAX+1):
        #### YOUR CODE HERE
        #### YOUR CODE HERE
        ## formula = ....
        SAT, assignment, runtime = solve(formula)
        if SAT:
            return (T,assignment)
        else:
            print("Formula for length " + str(T) + " is UNSAT")
    return None
