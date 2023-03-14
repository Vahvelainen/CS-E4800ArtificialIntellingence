import random

from envs.konquest import Universe
from agent_interface import AgentInterface
"""
Step 1 alphabeta

Setup: Alphabeta vs. Minmax with ~comparable time complexity and 10second timeout
Action: Implemented alphabeta pruning to provided iteratively deepening-minimax
Result: Alphabeta seems to be able to do one bit deeper search with similar branchign factor and time resource
        branching factor of 16 (starting state):
            ~ 0.2 second for Alphabeta with depth of 4
            ~ 2 seconds for Minimax with depth of 4
            ~ 2 second for Alphabeta with depth of 5
            ~ 23 second for Minimax with depth of 5

        games 19 - 11 to Alphabeta with depth of 5 vs Minimax depth of 4

        Both of the approaches times out when branching factors become especially high ->
        not good in defence as there is less potential for iterations in more complex defensice situations
        alltrough one could argue that its what happens in hopeless situations and good offense is best defence
"""


class AlphaBetaAgent(AgentInterface):
    """
    An agent who plays the Konquest game

    Methods
    -------
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """

    def __init__(self, depth: int = 4):
        self.depth = depth
        self.__player = None

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

        return {"agent name": "Alpha beta 1.0",  # COMPLETE HERE
                "student name": ["Leevi Vahvelainen"],  # COMPLETE HERE
                "student number": ["552956"]}  # COMPLETE HERE
    
    def heuristic(self, state: Universe):
        id = state.current_player_id
        my_ships = 0
        for planet in state.planets:
            if planet.owner == id:
                my_ships += planet.ships
        for fleet in state.fleets:
            if fleet.owner == id:
                my_ships += fleet.ships
        return my_ships

    def decide(self, state: Universe):
        """
        Get the value of each action by passing its successor to min_value
        function.
        """
        successors = state.successors()

        # Good ol' rnd suffle for the beginning
        # -> might be waste of time and will be tried to be picked with heuristics
        # Might be best use the math theory of sampling few and then picking best after them to limit the time
        random.shuffle(successors)
        best_action, _ = successors[0]

        #Player is us and maximazing so best =-inf
        max_value = float('-inf')
        for action, next_state in successors:
            action_value = self.min_value(next_state, self.depth - 1)
            if action_value > max_value:
                max_value = action_value
                best_action = action
        yield best_action

    def max_value(self, state: Universe, depth: int, alpha: int, beta: int):
        """
        Get the value of each action by passing its successor to min_value
        function. Return the maximum value of successors.
        
        `max_value()` function sees the game from players's perspective, trying
        to maximize the value of next state.
        
        NOTE: when passing the successor to min_value, `depth` must be
        reduced by 1, as we go down the Minimax tree.
        
        NOTE: the player must check if it is the winner (or loser)
        of the game, in which case, a large value (or a negative value) must
        be assigned to the state. Additionally, if the game is not over yet,
        but we have `depth == 0`, then we should return the heuristic value
        of the current state.
        """

        # Termination conditions
        is_winner = state.is_winner()
        if is_winner is not None:
            return is_winner * float('inf')
        if depth == 0:
            return self.heuristic(state)

        # If it is not terminated
        successors = state.successors()
        value = float('-inf')
        for _, next_state in successors:
            value = max(value, self.min_value(next_state, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def min_value(self, state: Universe, depth, alpha = float('-inf'), beta = float('inf')):
        """
        Get the value of each action by passing its successor to max_value
        function. Return the minimum value of successors.
        
        `min_value()` function sees the game from opponent's perspective, trying
        to minimize the value of next state.
        
        NOTE: when passing the successor to max_value, `depth` must be
        reduced by 1, as we go down the Minimax tree.

        NOTE: the opponent must check if it is the winner (or loser)
        of the game, in which case, a negative value (or a large value) must
        be assigned to the state. Additionally, if the game is not over yet,
        but we have `depth == 0`, then we should return the heuristic value
        of the current state.
        """

        # Termination conditions
        is_winner = state.is_winner()
        if is_winner is not None:
            return is_winner * float('-inf')
        if depth == 0:
            return -1 * self.heuristic(state)

        # If it is not terminated
        successors = state.successors()
        value = float('inf')
        for _, next_state in successors:
            value = min(value, self.max_value(next_state, depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value