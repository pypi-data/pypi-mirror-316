import pytest
import chess
from cc_engines import TourneyEngine
from cc_engines.random_engine import RandomEngine

def test_random_engine_creation():
    engine = RandomEngine()
    assert isinstance(engine, TourneyEngine)
    assert isinstance(engine, RandomEngine)

def test_random_engine_move_generation(sample_board):
    engine = RandomEngine()
    move = engine.getMove(sample_board)
    assert isinstance(move, chess.Move)
    assert move in sample_board.legal_moves