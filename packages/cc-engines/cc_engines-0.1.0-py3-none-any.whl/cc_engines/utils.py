import numpy as np

def cpToInt(score):
    """Convert chess score to integer centipawn value."""
    if score.is_mate():
        return np.sign(score.mate()) * 9999
    return score.cp

