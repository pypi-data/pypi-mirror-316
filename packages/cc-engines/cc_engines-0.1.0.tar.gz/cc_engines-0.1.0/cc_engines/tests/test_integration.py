import pytest
import chess
from cc_engines import StockfishEngine, MaiaEngine, LC0Engine

def test_engine_tournament(stockfish_path, lc0_path, maia_weights):
    engines = [
        StockfishEngine(stockfish_path=stockfish_path, movetime=0.1),
        MaiaEngine(model_path=maia_weights, lc0_path=lc0_path, movetime=0.1),
    ]
    
    board = chess.Board()
    moves_played = 0
    
    while not board.is_game_over() and moves_played < 10:
        current_engine = engines[moves_played % 2]
        move = current_engine.getMove(board)
        board.push(move)
        moves_played += 1
        
    assert moves_played > 0