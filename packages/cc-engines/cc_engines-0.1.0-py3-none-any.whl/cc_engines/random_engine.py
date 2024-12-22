import random
from .base import TourneyEngine

class _MoveHolder(object):
    def __init__(self, move):
        self.bestmove = move
        self.move = move

class _Random_Results(object):
    def __init__(self, move):
        self.move = move
        self.info = {}

class _RandomEngineBackend(object):
    def __init__(self):
        self.nextMove = None

    def position(self, board):
        self.nextMove = random.choice(list(board.legal_moves))

    def go(self, *args, **kwargs):
        return _MoveHolder(self.nextMove)

    def play(self, board, *args, **kwargs):
        return random.choice(list(board.legal_moves))

    def quit(self):
        pass

    def ucinewgame(self):
        pass

class RandomEngine(TourneyEngine):
    def __init__(self, engine = None, name = 'random', movetime = None, nodes = None, depth = None):
        super().__init__(_RandomEngineBackend(), name, movetime = movetime, nodes = nodes)

    def getMoveWithCP(self, board):
        return self.engine.play(board), 0

    def getMove(self, board):
        return self.engine.play(board)

    def getResults(self, board):
        return _Random_Results(self.engine.play(board))
