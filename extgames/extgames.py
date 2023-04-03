
import itertools

# Extensive form games
#
# The games are represented by using the classes Terminal, Move, ChanceMove.
#   Terminal(R):   A terminal node of a game, containing a payoff vector R
#   Move(P,S):     Move by agent P, with S containing all sub-games as a list.
#                      List elements are (A,N) where
#                         A is an action name (a string)
#                         N is the sub-game entered by choosing action A
#   ChanceMove(S): Random chance move, with S containing sub-games as a list.
#                      List elements are (P,A,N) where
#                         P is the probability of the subgame N
#                         A is the name of the chance move
#                         N is the subgame entered by choosing action A
#
# All these classes have the following methods:
#   eval(S,P) to evaluate strategy profile S with P as the path to the subgame.
#       S is a list with S[i] giving the strategy for player i
#          A strategy is a dictionary D with D[path] assigning an action to the sub-game
#             at the node reached by the action sequence 'path'.
#   decNodes(path) to list all nodes in which a player can take an action.
#       'path' is the sequence of action/move names on the path to the node.
#       It returns a list of triples (path,player,actions) where
#           path     is the list of action names that lead to the node
#           player   is the index of the player (0,1,...)
#           actions  is the list of action names available in that node

class Terminal:
    def __init__(self,payoffvector):
        self.payoffvector = payoffvector
    def eval(self,strategies,path):
        return self.payoffvector
    def decNodes(self,path):
        return []

# Concatenate a list of lists

def concat(ll):
    return list(itertools.chain.from_iterable(ll))

# Multiply each number in a list by a given number.

def vecmul(p,vector):
    return [ p*e for e in vector ]

class ChanceMove:
    def __init__(self,successors):
        self.successors = successors
    def eval(self,strategies,path):
        childpayoffs = [ vecmul(prob,successor.eval(strategies,path + [action])) for prob,action,successor in self.successors ]
        return [ sum([r[i] for r in childpayoffs ]) for i in range(len(childpayoffs[0])) ]
    def decNodes(self,path):
        return concat([ s.decNodes(path + [a]) for p,a,s in self.successors ])

# Turn a belief (a list of strings) to a hashable (a single string)

def nIndex(b):
    return "_".join(b)

class Move:
    def __init__(self,player,successors):
        self.player = player
        self.successors = successors
    def eval(self,strategies,path):
        strategy = strategies[self.player]
        action = strategy[nIndex(path)]
        for a,s in self.successors:
            if a == action:
                return s.eval(strategies,path + [action])
        print("Error: action not found")
        exit(1)
    def decNodes(self,path):
        return [(path,self.player,[ action for action,successor in self.successors ])] + concat([ s.decNodes(path + [a]) for a,s in self.successors ])

# Remove duplicates from a list with unhashable elements

def noDuplicates(l):
    return [k for k,v in itertools.groupby(sorted(l))]

# Intersection of a list with a set: those elements of the list that occur in the set

def listIntersect(l,s):
    return [ e for e in l if e in s ]

# Construct all possible strategies for every player.
# Iterate over all players p.
# 1. Identify nodes in the tree where it is player p's turn.
# 2. Identify "beliefs", which are all different types of
#    nodes that can be observationally distinguished.
#    Every node can be identified with the action/move sequence
#    leading to it, and every belief is such a sequence restricted
#    to those actions/moves the player can observe.
# 3. Generate all possible mappings belief -> action.
# 4. Generate corresponding mappings node -> action.
#      If belief B is associated with action A, and
#      the path to node N restricted to observable actions/moves
#      equals B, then associate action A with node N.
# These last mappings represent the strategies for player p.

def allStrategies(egame,observables):
    decNodes = egame.decNodes([])
    players = { player for path,player,actions in decNodes }

    # Which actions are possible in a node with a given belief

    def identifyActions(p,b):
        beliefactions = None
        for path,player,actions in decNodes:
            if player == p and listIntersect(path,observables[p]) == b:
                if beliefactions == None:
                    beliefactions = actions
                else:
                    if beliefactions != actions:
                        print("Observationally indistinguishable nodes have different actions")
                        exit(1)
        return beliefactions

    # List of pairs (player,strategies)
    allStrategies = dict()
    
    for p in players:
        print("STRATEGIES FOR PLAYER " + str(p) + ":")
        # Nodes where player can choose action
        decNodes4Player = { nIndex(path) for path,player,actions in decNodes if player == p }
        print("Decision nodes for player " + str(p) + ": " + ", ".join(decNodes4Player))
        # Beliefs = Prior actions observable to player in each node
        beliefs = noDuplicates([ listIntersect(path,observables[p]) for path,player,actions in decNodes if player == p ])
        print("Beliefs for player " + str(p) + ": " + ", ".join([ nIndex(b) for b in beliefs]))
        # Associate with each belief the set of actions player can take
        beliefActions = [ identifyActions(p,b) for b in beliefs ]
        actionCombinations = list(itertools.product(*beliefActions))
        strategies0 = [ list(zip(beliefs,actions)) for actions in actionCombinations ]
        strategies = []
        for strategy0 in strategies0:
            strategy = dict()
            for n in decNodes4Player:
                for b,action in strategy0:
                    if b == listIntersect(n.split("_"),observables[p]):
                        strategy[n] = action
                        continue
            # Show strategy
            print("PLAYER " + str(p) + " STRATEGY " + str(len(strategies)))
            for n in decNodes4Player:
                print("    Node " + str(n) + " action " + str(strategy[n]))
            strategies = strategies + [(len(strategies),strategy)]
        allStrategies[p] = strategies
    return allStrategies

# Reducing an extensive form game to a normal form game
# 1. Identify all strategies, N for player 0 and M for player 1.
# 2. Generate all N X M strategy combinations.
# 3. Determine the payoffs under every strategy combination.
# 4. Identify strictly dominated strategies, and eliminate them.
# 5. Show the remaining strategy combinations in the tabular form.

def reduceToNormalFormGame(egame,observables):
    # Find possible strategies for each player
    strategies = allStrategies(egame,observables)

    decNodes = egame.decNodes([])
    players = { player for path,player,actions in decNodes }

    if players != { 0,1 }:
        print("Considering 2-player games only!")
        exit(1)

    # All possible strategy combinations

    combinations = [ (n0,s0,n1,s1) for n0,s0 in strategies[0] for n1,s1 in strategies[1] ]

    # Evaluate each strategy combination: payoff vectors

    ecombinations = []
    for (n0,s0,n1,s1) in combinations:
        strategyprofile = dict()
        strategyprofile[0] = s0
        strategyprofile[1] = s1
        r0,r1 = egame.eval(strategyprofile,[])
        print("Strategy profile " + str(n0) + "," + str (n1) + " pay-offs: " + str(r0) + ", " + str(r1))
        ecombinations = ecombinations + [(n0,s0,n1,s1,r0,r1)]

    # All strategy indices for the two players

    st0 = { n for n,s in strategies[0] }
    st1 = { n for n,s in strategies[1] }

    # Show normal form game (before eliminating strictly dominated strategies)

    print("Normal form game:")
    showNormalForm(st0,st1,ecombinations)

    # Payoff player 0 for a given strategy combination

    def payoff0(n0,n1):
        for n00,s00,n11,s11,r00,r11 in ecombinations:
            if n0 == n00 and n1 == n11:
                return r00
        print("ERROR")
        exit(1)

    # Payoff of player 1 for a given strategy combination

    def payoff1(n0,n1):
        for n00,s00,n11,s11,r00,r11 in ecombinations:
            if n0 == n00 and n1 == n11:
                return r11
        print("ERROR")
        exit(1)

    # Is payoff for player 0 strategy n worse than for some other strategy,
    # for all opponent strategies?

    def dominated0(n):
        return any( all( payoff0(nn,n1) > payoff0(n,n1) for n1 in st1 ) for nn in st0 if n != nn)

    # Same for player 1

    def dominated1(n):
        return any( all( payoff1(n0,nn) > payoff1(n0,n) for n0 in st0 ) for nn in st1 if n != nn)

    # All strictly dominated strategies for both players

    dst0 = { n for n in st0 if dominated0(n) }
    dst1 = { n for n in st1 if dominated1(n) }

    print("Dominated strategies for player 0: " + ", ".join([ str(n) for n in dst0 ]))
    print("Dominated strategies for player 1: " + ", ".join([ str(n) for n in dst1 ]))

    # Strategies that are not strictly dominated

    sst0 = st0.difference(dst0)
    sst1 = st1.difference(dst1)

    # Show normal form game (after eliminating strictly dominated strategies)

    print("Normal form game after elimination of strictly dominated strategies:")
    showNormalForm(sst0,sst1,ecombinations)


# Show the strategies of a normal form game in the usual tabular form

def showNormalForm(rows,columns,ecombinations):
    # Column headings
    print("      ",end="")
    for column in sorted(columns):
        print("{0:11d} ".format(column),end="")
    print("")
    # The table
    for row in rows:
        print("{0:3d} | ".format(row),end="")
        for column in sorted(columns):
            for n0,s0,n1,s1,r0,r1 in ecombinations:
                if row == n0 and column == n1:
                    print ("{0:5.2f},{1:5.2f} ".format(r0,r1), end="")
        print("")
