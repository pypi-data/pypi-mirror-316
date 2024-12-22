# import chess.engine
# import subprocess
# from .base import TourneyEngine

# class StockfishEngine(TourneyEngine):
#     def __init__(self, stockfish_path, movetime=1.0, depth=30, name=None):
#         self.stockfish_path = stockfish_path
#         self.name = name or f"Stockfish d{depth} {movetime}"
        
#         engine = chess.engine.SimpleEngine.popen_uci(
#             [self.stockfish_path], 
#             stderr=subprocess.PIPE
#         )
#         engine.configure({'UCI_AnalyseMode': 'false'})
        
#         super().__init__(
#             engine=engine,
#             name=self.name,
#             movetime=movetime,
#             depth=depth
#         )
import chess.engine
import subprocess
from .base import TourneyEngine

class StockfishEngine(TourneyEngine):
    def __init__(self, stockfish_path, movetime=1.0, depth=30, name=None):
        self.stockfish_path = stockfish_path
        self.name = name or f"Stockfish d{depth} {movetime}"

        # Initialize the Stockfish engine
        engine = chess.engine.SimpleEngine.popen_uci(
            [self.stockfish_path],
            stderr=subprocess.PIPE
        )

        # Configure the engine with supported options
        engine.configure({
            'Threads': 2,  # Number of threads
            'Hash': 128,   # Hash table size in MB
            # Add more supported options here if needed
        })

        # Call the superclass constructor
        super().__init__(
            engine=engine,
            name=self.name,
            movetime=movetime,
            depth=depth
        )
