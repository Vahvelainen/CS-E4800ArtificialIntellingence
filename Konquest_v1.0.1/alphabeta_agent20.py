import random

from envs.konquest import Universe
from agent_interface import AgentInterface
"""
Step 1: alphabeta

    Action: Implemented alphabeta pruning to provided Minimax
    Result: Alphabeta seems to be able to do one bit deeper search with similar branching factor and time resource
            branching factor of 16 (starting state):
                ~ 0.2 second for Alphabeta with depth of 4
                ~ 2 seconds for Minimax with depth of 4
                ~ 2 second for Alphabeta with depth of 5
                ~ 23 second for Minimax with depth of 5

    Test: Alphabeta with depth of 5 vs Minimax depth of 4
        19 - 11 to Alphabeta, winrate 63%, slight improvement

        Both of the approaches times out when branching factors become especially high ->
        might not be good in defence as there might be less potential for iterations in more complex defensice situations
        alltrough one could argue that its what happens in hopeless situations and good offense is best defence

Step 2: heuristics

    Setup: Old heuristics vs. New heuristics with alphabeta with depth of 4 and 5second timeout (allows fast games and iteration)
           Earlier runs ran enough to see the difference or lack there of, later runs run 100 games  (10 games paraller) 

    Test 1: Count heuristic as a difference of own ships vs other ships in the game
            my_ships - other_ships vs. my_ships
    Result: 38 - 22, winrate 63%, slight benefit of considering the "rest of the world" with little added complexity. 

    Test 2: Count heuristic as a planet count * 10 + ship count, arguing that planets are more important than ships
            ( my_planets * 10 ) + my_ships vs. my_ships
    Result: 32 - 8. winrate 80% Very big difference with almost none added complexity

    Test 3: Same thing as before but with production instead of planets. Arguing that the production is the real KPI
            ( my_production * 10 ) + my_ships vs. my_ships
    Result: 33 - 7. Very similar as before but better in theory I would estimate

    Test 4: Previous heuristic with and with ship count taken into account
            ( my_production * 10 ) + my_ships vs. my_production
    Result: 56 - 44, ship count taken into account wins 56% percent of the time, implying it just migh not be completely useless variable

    Test 5: Heuristic from Test 3 vs. One with twice the relative weight on ship count
            This will determine the last tweaking with variables - the its time to try combining it to the wider situation
            ( my_production * 10 ) + my_ships vs. ( my_production * 5 ) + my_ships
    Result: 60-40, the old 10* heuristic won slightly implying that the ratio was around optimal in this setting

    Test 6: Same formula but now variables are differences of players production and ships instead of players individual assets
            (production_diff * 10) + ship_diff vs. ( my_production * 10 ) + my_ships
    Result: The difference-based heuristic lost by 46-54, practically a draw.

    Test 7: Same as before but difference to all the assets and not just enemy similary to Test 1
            (production_diff * 10) + ship_diff vs. ( my_production * 10 ) + my_ships
    Result: 61 - 39, very similar result to test 1

    Test 8: ratio vs. difference. Ratio of all production * 10 - ratio of all ships vs the formula from test 7
            (production_diff * 10) + ship_diff vs. (production_ratio * 10) + ship_ratio
    Result: 41-59 not sure if this is a fluke but we'll go with ratios

    Final test: Heuristic from Test 8 compared to my_ship count
                (production_ratio * 10) + ship_ratio vs. my_ships
                70 - 30, curiously worse than test 2 ratio, but that test done with full 100 runs gives similar result of very similar 68 - 32
                implying the nyance between more sophisticated formlas might not be very large in bigger picture


Step 3: Heuristic que / continous
        Is using heuristics to que for states better

Step 4: compare to monte carlo methods if time

"""


class AlphaBetaAgent2(AgentInterface):
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

        return {"agent name": "Alpha beta 2.0",  # COMPLETE HERE
                "student name": ["Leevi Vahvelainen"],  # COMPLETE HERE
                "student number": ["552956"]}  # COMPLETE HERE
    
    def heuristic(self, state: Universe):
        my_id = state.current_player_id
        my_ships = 0
        my_production = 0

        # enemy_id = state.players[ state.current_player - 1 ].id_
        all_ships = 0
        all_production = 0

        for planet in state.planets:
            if planet.owner == my_id:
                my_ships += planet.ships
                my_production += planet.info.production
            all_ships += planet.ships
            all_production += planet.info.production
        for fleet in state.fleets:
            if fleet.owner == my_id:
                my_ships += fleet.ships
            all_ships += fleet.ships

        production_ratio = my_production / all_production
        ship_ratio = my_ships / all_ships

        return (production_ratio * 10) + ship_ratio

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