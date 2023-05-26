from components.component import Component
from math import sqrt
from util.math import Vector2
from actors.actor import Actor
from pygame import Rect
from enum import Enum
from components.rectfigure import RectFigure

class Collision(Component):
    class CollSide(Enum):
        NONE = 0
        TOP = 1
        BOTTOM = 2
        LEFT = 3
        RIGHT = 4
    
    def __init__(self, actor: Actor):
        super().__init__(actor)
        self.rect: Rect = Rect(0, 0, 0, 0)
        self.rect.center = (self.actor.position[0], self.actor.position[1])
        self.colliding_check = True
        self.excludes: list[Actor] = []
        self.sprite_rect = RectFigure(self.actor, 20)
        self.sprite_rect.visible = False
    
    def set_size(self, height: int, width: int):
        self.rect.height = height
        self.rect.width = width
        self.sprite_rect.set_properties(width, height, (0, 255, 0))
    
    def set_collision(self, collision_on: bool):
        self.colliding_check = collision_on
    
    def exclude(self, exclude: Actor):
        self.excludes.append(exclude)
    
    def clear_excludes(self):
        self.excludes.clear()
    
    def get_center(self):
        return self.actor.position

    def intersect(self, c: 'Collision'):
        if not self.colliding_check or c.actor in self.excludes:
            return False
        self.rect.center = self.actor.position
        c.rect.center = c.actor.position
        return self.rect.colliderect(c.rect)

    def get_min_overlap(self, c: 'Collision') -> tuple[CollSide, Vector2]:
        if not self.intersect(c):
            return (Collision.CollSide.NONE, Vector2())
        our_min = self.rect.topleft
        our_max = self.rect.bottomright
        their_min = c.rect.topleft
        their_max = c.rect.bottomright
        top = their_min[1] - our_max[1]
        bottom = their_max[1] - our_min[1]
        right = their_max[0] - our_min[0]
        left = their_min[0] - our_max[0]
        dists = [top, bottom, left, right]
        dists: list[float] =  list(map(lambda n: abs(n), dists))
        dists.sort()
        if dists[0] == abs(top):
            return (Collision.CollSide.TOP, Vector2(0, top))
        elif dists[0] == abs(bottom):
            return (Collision.CollSide.BOTTOM, Vector2(0, bottom))
        elif dists[0] == abs(right):
            return (Collision.CollSide.RIGHT, Vector2(right, 0))
        else:
            return (Collision.CollSide.LEFT, Vector2(left, 0))

