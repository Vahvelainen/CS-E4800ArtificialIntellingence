from iterative_deepening import IterativeDeepening
from alphabeta_agent import AlphaBetaAgent

#using version 1.0 for now before starting the real action

class IDAlphaBetaAgent(IterativeDeepening):
    def __init__(self):
        super().__init__(AgentClass=AlphaBetaAgent)