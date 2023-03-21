from envs.konquest import Universe
from agent_interface import AgentInterface
import math
import random

# First actual succesfull tests with sanitychecking the algorithm works:
# 43 / 7 (of 50), wins 86% of the time on 4s turns

# Test with heuristic vs random paths MCTS
# Heuristic lost 7 / 41 (of 48) on 4s turns
# I assume tha the extra computation isn't worth it

# Then, tinker with the saving / pruning possibility
# ie. each state would have scores and successors to correspond
# tinkered -> comparing states not directly possible / too complicated

# tested against imporved alphabeta with good heuristics
# 50 games, 2 second turns
# 12 / 38 to aplhabeta
# 14 / 36 in 4 second turns "ei jatkoon"



class MonteCarloTS(AgentInterface):
    """
    An agent who plays the Konquest game

    Methods
    -------
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """
    def __init__(self):
        # Start state recorded from deiciding
        self.start_state = None
        # Dictionary of lists for scores for all the states
        self.state_scores = {}
        # Dictionary for recording successors for prunign and stuff
        self.state_successors = {}

    @staticmethod
    def info():
        """
        Return the agent's information

        Returns
        -------
        Dict[str, str]
            `agent name` is the agent's name
            `student name` is the list team members' names
            `student number` is the list of student numbers of the team members
        """
        # -------- Task 1 -------------------------
        # Please complete the following information
        # NOTE: Please try to pick a unique name for you agent. If there are
        #       some duplicate names, we have to change them.

        return {"agent name": "MonteCarltoTS",  # COMPLETE HERE
                "student name": ["?"],  # COMPLETE HERE
                "student number": ["?"]}  # COMPLETE HERE

    def makePath(self, state: Universe):

        # Goal check / I have absolutely no clue how this is working but it seems to win
        is_winner = state.is_winner()
        if is_winner is not None:
            if state.current_player_id == self.start_state.current_player_id:
                return is_winner
            else:
                return is_winner * -1
            
        #The investigated states of current state
        seen_successors = []
        if state in self.state_successors.keys():
            seen_successors = self.state_successors[state]

        successors = state.successors()
        #Random suffle worked better than heuristics
        random.shuffle(successors)

        i = 0
        best_state = None
        
        while not best_state:

            # Checking for previously unseen states first is the optimal way because:
            # 1. ) Most of the states visited will be new
            # 2. ) Going trough the successors before UCB1 selection is needed anyway

            if not successors[i][1] in seen_successors:
                best_state = successors[i][1]
                self.state_scores[best_state] = []
                seen_successors.append(best_state)

            elif i+1 < successors(len):  
                i += 1
            
            #If all the successors are seen before, do UCB1 decision
            else:
                #This whole thing could be more DRY
                successors_scores = []
                for _, successor_state in successors:
                    successors_scores.append( self.state_scores[ successor_state ] )
                UCB1_vals = self.UCB1( successors_scores )
                best_state = successors[ UCB1_vals.index( max(UCB1_vals) ) ][0]

        result = self.makePath(best_state)
        self.state_scores[best_state].append( result )

        return result
    
    def UCB1(self, sequences):
        N = sum( len(seq) for seq in sequences) #the number of round
        UCB1_Values = []
        for seq in sequences:
            Nt_a = len(seq) #number of times the option is chosen
            Qt_a = sum(seq) / Nt_a #the average return of the option
            ucb1_val = Qt_a + math.sqrt( (2 * math.log(N)) / Nt_a )
            UCB1_Values.append(ucb1_val) 
        return UCB1_Values


    def decide(self, state: Universe):
        """
        Generate a sequence of increasingly preferable actions

        Given the current `state`, this function should choose the action that
        leads to the agent's victory.
        However, since there is a time limit for the execution of this function,
        it is possible to choose a sequence of increasing preferable actions.
        Therefore, this function is designed as a generator; it means it should
        have no return statement, but it should `yield` a sequence of increasing
        good actions.

        IMPORTANT: If no action is yielded within the time limit, the game will
        choose a random action for the player.

        NOTE: You can find the possible actions and next states by using
              the `successors()` method of the `state`. In other words,
              `state.successors()` return a list of pairs of `action` and its
              corresponding next state.

        Parameters
        ----------
        state: Universe
            Current state of the game

        Yields
        ------
        action
            the chosen `action`
        """

        # It would be cool if agent would remember the states from last game
        # unfortunately the game couldnt compare the states to do that

        successorActionStates = state.successors()
        successors = list( map( lambda x: x[1] ,successorActionStates ) )

        # For goal checking or something
        self.start_state = state

        # Dictionary for recording scores for every state including the first successors
        self.state_scores = {}

        # Dictionary for recording successors for prunign and stuff
        self.state_successors = {}

        # One round for the succerssor states
        for next_state in successors:
            result = self.makePath(next_state)
            self.state_scores[ next_state ] = [ result ] #this could happen in makepath


        while True:
            # Select currently best yielding action
            successor_scores = []
            successor_averages = []
            for next_state in successors:
                scores = self.state_scores[next_state] 
                successor_scores.append(scores)
                successor_averages.append( sum(scores) / len(scores) )
            yield successorActionStates[ successor_averages.index( max(successor_averages) ) ][0]
            
            #Get the successor state to examine based on UCB1
            UCB1_vals = self.UCB1( successor_scores )
            probe_deeper = successors[ UCB1_vals.index( max(UCB1_vals) ) ]

            # Do the one itearation
            new_score = self.makePath(probe_deeper)
            self.state_scores[ probe_deeper ].append(new_score)
