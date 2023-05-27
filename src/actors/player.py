from actors.actor import Actor
from util.math import Vector2
from components.sprite import AnimatedSprite
from components.playermove import PlayerMove
from components.collision import Collision
from components.follownodes import FollowNodes
from actors.collider import Collider
import pygame

class Player(Actor):
    def __init__(self, game: 'Game', starting_position: Vector2, anim: str):
        super().__init__(game)
        self.position = starting_position
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim)
        self.collision = Collision(self)
        self.collision.set_size(0, 0)
        move = PlayerMove(self)
        self.e_pressed: bool = False
        self.f_pressed: bool = False
        self.o_pressed: bool = False
        self.attack1: None|Collider = None
        self.attack1_cd: float = 0.0
        self.attack1_lifetime = 0.0
    
    def on_process_input(self, keys: list[bool]):
        if not self.e_pressed and keys[pygame.K_e] and self.attack1_cd <= 0.0:
            move = self.get_component(PlayerMove)
            direction = move.get_direction()
            big_dim: int = 200
            small_dim: int = 200
            offset = big_dim/2 + 20
            width: int = 0
            height: int = 0
            offset_from_player: Vector2 = Vector2()
            if direction == PlayerMove.Direction.RIGHT or direction == PlayerMove.Direction.LEFT:
                width = big_dim
                height = small_dim
                polarity = 1 if direction == PlayerMove.Direction.RIGHT else -1
                offset_from_player = Vector2(polarity * offset, 0)
            if direction == PlayerMove.Direction.DOWN or direction == PlayerMove.Direction.UP:
                width = small_dim
                height = big_dim
                polarity = 1 if direction == PlayerMove.Direction.DOWN else -1
                offset_from_player = Vector2(0, polarity * offset)
            self.attack1 = Collider(self.game, self.position + offset_from_player, width, height, True, (0, 0, 255))
            self.attack1_lifetime = 0.1
            self.attack1_cd = 2.0
        
        if not self.f_pressed and keys[pygame.K_f]:
            for c in self.game.enemies:
                    c.damage(1.5)
        
        if not self.o_pressed and keys[pygame.K_o]:
            cols = [self.game.enemies, self.game.colliders, self.game.npcs]
            for cs in cols:
                for c in cs:
                    col: Collision = c.collision
                    col.sprite_rect.visible = not col.sprite_rect.visible
                    follow_nodes: FollowNodes = c.get_component(FollowNodes)
                    if follow_nodes:
                        follow_nodes.visible_nodes = not follow_nodes.visible_nodes
            self.collision.sprite_rect.visible = not self.collision.sprite_rect.visible
    
        self.e_pressed = keys[pygame.K_e]
        self.f_pressed = keys[pygame.K_f]
        self.o_pressed = keys[pygame.K_o]
    
    def on_update(self, dt: float):
        self.attack1_cd -= dt
        if self.attack1:
            self.attack1_lifetime -= dt
            if self.attack1_lifetime <= 0.0:
                self.attack1.state = Actor.State.Destroyed
                return
            for c in self.game.enemies:
                if self.attack1.collision.intersect(c.collision):
                    c.stop(2)
