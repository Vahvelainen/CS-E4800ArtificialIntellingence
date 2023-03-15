from typing import Type
from random import seed

from game import Game
from envs.konquest import Universe
from envs.visualizer import Visualizer

# Importing Agents
from agent_interface import AgentInterface
from random_agent import RandomAgent
from minimax_agent import MinimaxAgent
from id_minimax_agent import IDMinimaxAgent
from markov_agent import MarkovAgent
from alphabeta_agent10 import AlphaBetaAgent1
from alphabeta_agent20 import AlphaBetaAgent2
from id_alphabeta_agent import IDAlphaBetaAgent

import sys

# from agent import Agent    # After completing your agent, you can uncomment this line

#filename = 'Documents/GitHub/CS-E4800ArtificialIntellingence/Konquest_v1.0.1/testresults.txt'
filename = sys.argv[1]

# If you want the reproducibility uncomment the following line
# seed(13731367)
NEUTRAL_PLANETS_COUNT =  4


def main():

    ############### Set the players ###############
    players = [AlphaBetaAgent1, AlphaBetaAgent2]
    ###############################################

    #Runs two games after each other and swicthes positios in between
    player_one_results = []
    results = [0, 0]
    initial_state = Universe([player_name(p) for p in players],
                                NEUTRAL_PLANETS_COUNT)
    for round in range(len(players)):
        print( "########################################################")
        print("#{: ^54}#".format(f"ROUND {round}"))
        print( "########################################################")
        players_instances = [p() for p in players]
        # Timeout for each move. Don't rely on the value of it. This
        # value might be changed during the tournament.
        timeouts = [5, 5]

        game = Game(players_instances)
        new_round = initial_state.clone().initialize()

        winners = game.play(new_round,
                            output=True,
                            visualizer=None,
                            timeout_per_turn=timeouts)
        
        #Game ended
        if len(winners) == 1:
            results[winners[0]] += 1

        print()
        print(f"Result) {player_name(players[0])}: {results[0]} - "
            f"{player_name(players[1])}: {results[1]}")
        print("########################################################")
        
        #The will be wrtiten to a file
        # True if index == winner meaning the first player won
        player_one_results.append( winners[0] == round )

        # Rotating players for the next rounds
        initial_state.rotate_players()
        players.append(players.pop(0))
        results.append(results.pop(0))

    #Write player one result into a wfile
    for result in player_one_results:
        with open(filename, 'a') as the_file:
            the_file.write( str( result ) + '\n')


def player_name(player: Type[AgentInterface]):
    return player().info()['agent name']


if __name__ == "__main__":
    import platform
    if platform.system() == "Darwin":
        import multiprocessing
        multiprocessing.set_start_method('spawn')

    try:
        main()
    except BrokenPipeError as e:
        print("Broken Pipe Error:", e)
    except EOFError as e:
        print("EOF Error:", e)