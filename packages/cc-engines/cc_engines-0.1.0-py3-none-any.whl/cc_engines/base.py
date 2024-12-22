import chess
import chess.engine
import concurrent.futures
import numpy as np
from .utils import cpToInt

class TourneyEngine(object):
    def __init__(self, engine, name, movetime = None, nodes = None, depth = None):
        self.engine = engine
        self.name = f"{type(self).__name__} {name}"
        self.movetime = movetime
        self.depth = depth
        self.nodes = nodes

        self.limits = chess.engine.Limit(
            time = movetime,
            depth = depth,
            nodes = nodes,
        )

    def __repr__(self):
        return f"<{self.name}>"

    def __str__(self):
        return self.name

    def getAnalyzeMoves(self, board, limits = chess.engine.Limit(time=2.0, depth=30), num_moves=4):
        return self.engine.analyse(
            board,
            limits,
            info = chess.engine.INFO_ALL,
            multipv = num_moves)
    
    def getTopMovesCP(self, board, num_moves):
        results = self.engine.analyse(
                board,
                self.limits,
                info = chess.engine.INFO_ALL,
                multipv = num_moves,
                )
        ret_dat = []
        for m_dict in results:
            try:
                cp = cpToInt(m_dict['score'])
            except KeyError:
                cp = 0
            ret_dat.append((m_dict['pv'][0].uci(), cp))
        return ret_dat

    def getMoveWithCP(self, board):
        result = self.getResults(board)
        try:
            cp = cpToInt(result.info['score'])
        except KeyError:
            cp = 0
        return result.move, cp

    def getMove(self, board):
        result = self.getResults(board)
        return result.move

    def getResults(self, board):
        return self.engine.play(board, self.limits, game = board, info = chess.engine.INFO_ALL)

    def getBoardChildren(self, board):
        moves_ret = {}
        for m in board.legal_moves:
            b_m = board.copy()
            b_m.push(m)
            r = self.engine.analyse(b_m, limit=self.limits, info = chess.engine.INFO_ALL, multipv = None)
            moves_ret[str(m)] = r
        return moves_ret

    def getMeanEval(self, board, depth):
        scores = []
        if depth <= 0:
            cVals = self.getBoardChildren(board)
            for m, d in cVals.items():
                scores.append(cpToInt(d['score']))
        elif depth % 2 == 1:
            b_m = board.copy()
            m = self.getMove(b_m)
            b_m.push(m)
            return self.getMeanEval(b_m, depth - 1)
        else:
            for m in board.legal_moves:
                b_m = board.copy()
                b_m.push(m)
                scores.append(self.getMeanEval(b_m, depth - 1))

        return np.mean(scores)

    def depthMovesSearch(self, board, depth = 2):
        moves = {}
        for m in sorted(board.legal_moves):
            b_m = board.copy()
            b_m.push(m)
            moves[str(m)] = self.getMeanEval(b_m, depth - 1)
        return max(moves.items(), key = lambda x : x[1])

    def __del__(self):
        try:
            try:
                self.engine.quit()
            except (chess.engine.EngineTerminatedError, concurrent.futures._base.TimeoutError):
                pass
        except AttributeError:
            pass