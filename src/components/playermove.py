from components.component import Component
from components.collision import Collision
from components.sprite import AnimatedSprite
from util.interfaces import IActorWithCollision
from util.math import Vector2, clamp
from util.controls import UP_CONTROL, DOWN_CONTROL, RIGHT_CONTROL, LEFT_CONTROL, control_pressed
from enum import Enum
import pygame


Event = pygame.event.Event

class PlayerMove(Component):

    PLAYER_SPEED: float = 356.0

    class Direction(Enum):
        UP = 0
        DOWN = 1
        RIGHT = 2
        LEFT = 3

    def __init__(self, player: 'Player'):
        super().__init__(player)
        self.walking: bool = False
        self.facing_dir: PlayerMove.Direction = PlayerMove.Direction.UP
        self.player_anim: AnimatedSprite = self.actor.get_component(AnimatedSprite)
        self.player_collision: Collision = self.actor.get_component(Collision)
        self.player_anim.set_animation('up', True)
        dim = self.player_anim.get_col_dim()
        if dim:
            self.player_collision.set_size(dim.y, dim.x)
        self.direction = Vector2()
    
    def process_input(self, keys: list[bool]):
        self.direction = Vector2()
        if control_pressed(UP_CONTROL, keys):
            self.walking = True
            self.facing_dir = PlayerMove.Direction.UP
            self.direction = Vector2(0, -1)
        elif control_pressed(DOWN_CONTROL, keys):
            self.walking = True
            self.facing_dir = PlayerMove.Direction.DOWN
            self.direction = Vector2(0, 1)
        elif control_pressed(RIGHT_CONTROL, keys):
            self.walking = True
            self.facing_dir = PlayerMove.Direction.RIGHT
            self.direction = Vector2(1, 0)
        elif control_pressed(LEFT_CONTROL, keys):
            self.walking = True
            self.facing_dir = PlayerMove.Direction.LEFT
            self.direction = Vector2(-1, 0)
        else:
            self.walking = False
        if self.direction == Vector2():
            self.walking = False
        
    def get_direction(self) -> Direction:
        return self.facing_dir
    
    def update_animations(self):
        if self.facing_dir == PlayerMove.Direction.DOWN:
            self.player_anim.set_animation('down', not self.walking)
        elif self.facing_dir == PlayerMove.Direction.UP:
            self.player_anim.set_animation('up', not self.walking)
        elif self.facing_dir == PlayerMove.Direction.LEFT:
            self.player_anim.set_animation('left', not self.walking)
        else:
            self.player_anim.set_animation('right', not self.walking)
        col = self.player_anim.get_col_dim()
        self.player_collision.set_size(col.y, col.x)
    
    def update(self, dt: float):
        self.update_animations()
        old_position = self.actor.position.copy()
        velocity = PlayerMove.PLAYER_SPEED * self.direction
        self.actor.position += velocity * dt
        player_collision: Collision = self.actor.get_component(Collision)
        collided = False
        collided_too_little = True
        all_collisioners: list[list[IActorWithCollision]] = [self.get_game().colliders, self.get_game().enemies, self.get_game().npcs]
        for c in all_collisioners:
            for coll in c:
                if not coll.collision.colliding_check or self.actor in coll.collision.excludes:
                    continue
                side, offset = player_collision.get_min_overlap(coll.collision)
                if side != Collision.CollSide.NONE:
                    collided = True
                    offset_mag = offset.length()
                    if offset_mag >= 8.0:
                        collided_too_little = False
                        self.actor.position += offset
        if collided and collided_too_little:
            self.actor.position = old_position