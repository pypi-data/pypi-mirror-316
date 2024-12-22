import pytest
import chess
from pathlib import Path

@pytest.fixture
def sample_board():
    return chess.Board()

@pytest.fixture
def sample_fen():
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@pytest.fixture
def stockfish_path():
    # Update this path according to your system
    return str(Path("path/to/stockfish"))

@pytest.fixture
def lc0_path():
    # Update this path according to your system
    return str(Path("path/to/lc0"))

@pytest.fixture
def maia_weights():
    # Update this path according to your system
    return str(Path("path/to/maia/weights"))
