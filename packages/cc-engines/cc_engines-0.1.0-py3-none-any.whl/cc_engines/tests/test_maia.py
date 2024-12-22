import pytest
from cc_engines import MaiaEngine

def test_maia_creation(maia_weights, lc0_path):
    engine = MaiaEngine(
        model_path=maia_weights,
        lc0_path=lc0_path,
        movetime=0.1
    )
    assert isinstance(engine, MaiaEngine)