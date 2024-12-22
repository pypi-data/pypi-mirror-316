import os
import chess.engine
import subprocess
from .base import TourneyEngine

class LC0Engine(TourneyEngine):
    def __init__(self, 
                 weights_path,
                 lc0_path,
                 nodes=None,
                 movetime=1.0,
                 threads=1,
                 backend='blas',
                 backend_opts='',
                 name=None,
                 noise=False,
                 extra_flags=None,
                 verbose=False,
                 temperature=0,
                 temp_decay=0):
        
        self.weights_path = weights_path
        self.lc0_path = lc0_path
        
        cmd = [
            self.lc0_path,
            f'--weights={weights_path}',
            f'--threads={threads}',
            f'--backend={backend}',
            f'--backend-opts={backend_opts}',
            f'--temperature={temperature}',
            f'--tempdecay-moves={temp_decay}'
        ]
        
        if noise:
            cmd.append('--noise')
            if isinstance(noise, float):
                cmd.append(f'--noise-epsilon={noise}')
        
        if verbose:
            cmd.append('--verbose-move-stats')
            
        if extra_flags:
            cmd.extend(extra_flags)
            
        engine = chess.engine.SimpleEngine.popen_uci(
            cmd,
            stderr=subprocess.DEVNULL
        )
        
        if name is None:
            name = f"{os.path.basename(self.weights_path)[:-6]} {movetime}"
            
        super().__init__(
            engine=engine,
            name=name,
            movetime=movetime,
            nodes=nodes
        )

class HaibridEngine(LC0Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, isHai=True)

class LeelaEngine(LC0Engine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, isHai=False)