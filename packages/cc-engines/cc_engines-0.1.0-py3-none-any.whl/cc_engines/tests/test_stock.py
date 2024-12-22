import pytest
from cc_engines import StockfishEngine

def test_stockfish_creation(stockfish_path):
    engine = StockfishEngine(
        stockfish_path=stockfish_path,
        movetime=0.1,
        depth=10
    )
    assert isinstance(engine, StockfishEngine)

def test_stockfish_move_generation(stockfish_path, sample_board):
    engine = StockfishEngine(
        stockfish_path=stockfish_path,
        movetime=0.1,
        depth=10
    )
    move = engine.getMove(sample_board)
    assert move in sample_board.legal_moves