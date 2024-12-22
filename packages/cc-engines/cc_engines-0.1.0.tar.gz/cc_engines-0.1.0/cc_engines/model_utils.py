import os
import glob
from pathlib import Path

class Trained_Model:
    """Class to handle trained model weights management."""
    
    def __init__(self, model_path):
        """
        Initialize with path to model weights.
        
        Args:
            model_path (str): Path to the model weights directory or file
        """
        self.model_path = Path(model_path)
        
        # If path is a directory, look for weight files
        if self.model_path.is_dir():
            self.weight_files = sorted(
                glob.glob(str(self.model_path / "*.pb")),
                key=os.path.getmtime
            )
        else:
            self.weight_files = [str(self.model_path)]
            
        if not self.weight_files:
            raise ValueError(f"No weight files found in {model_path}")

    def getMostTrained(self):
        """Get the path to the most recently modified weights file."""
        return self.weight_files[-1]
    
    def getAllWeights(self):
        """Get list of all weight files sorted by modification time."""
        return self.weight_files