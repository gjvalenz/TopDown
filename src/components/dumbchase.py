from components.approachposition import ApproachPosition

class DumbChase(ApproachPosition):
    def __init__(self, actor: 'Actor', speed: float, stop_when_close: bool = False, close_dist: float = 0.0):
        super().__init__(actor, speed, stop_when_close, close_dist)
        self.target : 'Actor'|None = None
    
    def set_target(self, target: 'Actor'):
        self.target = target
    
    def update(self, dt: float):
        if not self.target:
            return
        self.set_position(self.target.position)
        super().update(dt)
