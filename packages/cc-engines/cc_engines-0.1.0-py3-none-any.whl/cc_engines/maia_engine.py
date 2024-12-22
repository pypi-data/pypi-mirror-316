from .lc import LC0Engine
from .model_utils import Trained_Model

class MaiaEngine(LC0Engine):
    def __init__(self, model_path, **kwargs):
        self.Model = Trained_Model(model_path)
        kwargs['weights_path'] = self.Model.getMostTrained()
        super().__init__(**kwargs)

class OldMaiaEngine(LC0Engine):
    def __init__(self, model_path, **kwargs):
        kwargs['weights_path'] = model_path
        super().__init__(lc0_path='lc0', **kwargs)

class NewMaiaEngine(LC0Engine):
    def __init__(self, model_path, **kwargs):
        kwargs['weights_path'] = model_path
        super().__init__(lc0_path='lc0_23', **kwargs)

