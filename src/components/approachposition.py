from components.component import Component
from components.collision import Collision
from util.math import Vector2
from math import inf

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

class ApproachPosition(Component):

    def __init__(self, actor: 'Actor', speed: float, stop_when_close: bool = False, close_dist: float = 0.0):
        super().__init__(actor)
        self.position: Vector2|None = None
        self.stop: bool = stop_when_close
        self.stop_dist: float = close_dist
        self.speed: float = speed
        self.stopped: bool = False
    
    def set_position(self, target: Vector2):
        self.position = target
        self.stopped = False
    
    def get_follow_direction(self, true_dir: Vector2) -> Vector2:
        dirs = [UP, DOWN, LEFT, RIGHT]
        dir = DOWN
        smallest_l = inf
        for d in dirs:
            if (d - true_dir).length() < smallest_l:
                dir = d
                smallest_l = (d - true_dir).length()
        return dir
    
    def update_animations(self, dir: Vector2, stopped: bool) -> Vector2:
        if dir == Vector2(0, 1):
            self.actor.animated.set_animation('down', stopped)
        elif dir == Vector2(0, -1):
            self.actor.animated.set_animation('up', stopped)
        elif dir == Vector2(-1, 0):
            self.actor.animated.set_animation('left', stopped)
        else:
            self.actor.animated.set_animation('right', stopped)
        col = self.actor.animated.get_col_dim()
        self.actor.collision.set_size(col.y, col.x)
    
    def update(self, dt: float):
        old_position = self.actor.position.copy()
        true_dir = (self.position - self.actor.position).normalize()
        dir = self.get_follow_direction(true_dir)
        stop_cond = self.position.distance_to(self.actor.position) <= self.stop_dist
        if hasattr(self.actor, 'animated'):
            self.update_animations(dir, stop_cond)
        if not self.position or self.stopped:
            return
        if self.stop and stop_cond:
            self.stopped = True
            return
        self.actor.position += true_dir * dt * self.speed
        collider: Collision = self.actor.get_component(Collision)
        if collider:
            all_collidables = self.get_game().colliders.copy()
            all_collidables.append(self.get_game().player)
            collided = False
            for c in all_collidables:
                if c.collision == collider:
                    continue
                side, offset = collider.get_min_overlap(c.collision)
                if side != Collision.CollSide.NONE:
                    #self.acposition += offset
                    collided = True
            if collided:
                self.actor.position = old_position
            

