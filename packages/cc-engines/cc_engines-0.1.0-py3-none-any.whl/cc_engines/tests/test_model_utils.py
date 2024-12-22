import pytest
import os
import tempfile
from pathlib import Path
from cc_engines.model_utils import Trained_Model

def test_trained_model_single_file():
    with tempfile.NamedTemporaryFile(suffix='.pb') as tf:
        model = Trained_Model(tf.name)
        assert model.getMostTrained() == tf.name
        assert len(model.getAllWeights()) == 1

def test_trained_model_directory():
    with tempfile.TemporaryDirectory() as td:
        # Create some dummy weight files
        weight_files = []
        for i in range(3):
            path = Path(td) / f"weights_{i}.pb"
            path.touch()
            weight_files.append(str(path))
            # Sleep to ensure different modification times
            import time
            time.sleep(0.1)
        
        model = Trained_Model(td)
        assert model.getMostTrained() == weight_files[-1]
        assert len(model.getAllWeights()) == 3

def test_trained_model_no_weights():
    with tempfile.TemporaryDirectory() as td:
        with pytest.raises(ValueError):
            Trained_Model(td)