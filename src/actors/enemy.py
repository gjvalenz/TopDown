from actors.actor import Actor
from util.math import Vector2
from components.sprite import Sprite
from actors.node import Node
from components.collision import Collision
from components.spriteflash import SpriteFlash
from components.follownodes import FollowNodes
from components.dumbchase import DumbChase
from components.animatedsprite import AnimatedSprite
from util.event import Event, EventManager

class Enemy(Actor):
    def __init__(self, game: 'Game', startingPosition: Vector2, texture: str):
        super().__init__(game)
        self.position = startingPosition
        if texture:
            self.texture = texture
            self.sprite = Sprite(self, 50)
            self.sprite.load_texture(texture)
            rect = self.sprite.texture.get_rect()
        self.collision = Collision(self)
        if texture:
            self.collision.set_size(rect.height, rect.width)
        game.add_enemy(self)
        self.flash = SpriteFlash(self, 4)
        self.stop_timer = 0.0
    
    def start_again(enemy: 'Enemy'):
        enemy.state = Actor.State.Active
    
    def turn_on_collision(enemy: 'Enemy'):
        enemy.collision.clear_excludes()
    
    def stop(self, time: float):
        self.state = Actor.State.Paused
        EventManager.get_instance().add_event(Event(Enemy.start_again, time, self))
    
    def damage(self, damage: int):
        self.flash.start_flash(0.5)
        self.collision.exclude(self.game.player)
        EventManager.get_instance().add_event(Event(Enemy.turn_on_collision, 0.5, self))
    


class FixedMovingEnemy(Enemy):
    def __init__(self, game: 'Game', startingPosition: Vector2, anim_src: str, nodes: list[Node], speed: float):
        super().__init__(game, startingPosition, None)
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim_src)
        FollowNodes(self, nodes, speed)
        for n in nodes:
            n.attach_parent(self)

class DumbChaseEnemy(Enemy):
    def __init__(self, game: 'Game', startingPosition: Vector2, anim_src: str, close_dist: float, speed: float):
        super().__init__(game, startingPosition, None)
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim_src)
        if close_dist == 0.0:
            dc = DumbChase(self, speed, False, False)
            dc.set_target(game.player)
        else:
            dc = DumbChase(self, speed, True, close_dist)
            dc.set_target(game.player)