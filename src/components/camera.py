from components.component import Component
from util.math import Vector2, clamp
from util.util import max_x, max_y

class Camera(Component):
    def __init__(self, actor: 'Actor'):
        super().__init__(actor, 101)
        self.game = self.get_game()
    
    def update(self, dt: float):
        new_camera_pos = self.actor.position - (Vector2(max_x/2, max_y/2))
        dim: Vector2 = self.game.map_dim
        self.game.camera = Vector2(clamp(-dim.x, new_camera_pos.x, dim.x-max_x), clamp(-dim.y, new_camera_pos.y, dim.y-max_y))
