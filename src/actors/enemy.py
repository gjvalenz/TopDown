from actors.actor import Actor
from util.math import Vector2
from components.sprite import AnimatedSprite, Sprite
from actors.node import Node
from components.collision import Collision
from components.spriteflash import SpriteFlash
from components.follownodes import FollowNodes
from components.dumbchase import DumbChase
from util.event import Event, EventManager
from util.interfaces import IActorWithCollision, IActorWithAnimated, IActorWithSprite
from util.observer import EnemyInstance
from util.quest import QuestManager

class Enemy(Actor, IActorWithCollision, EnemyInstance):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 collision: Vector2, scale: float = 1.0, name=''):
        super().__init__(game, name)
        q = QuestManager.get_instance()
        self.attach(q)
        self.position = starting_position
        self.scale = scale
        self.collision = Collision(self)
        self.collision.set_size(collision.y, collision.x)
        self.flash = SpriteFlash(self, 4)
        self.stunned = False
        game.add_enemy(self)
        
    def start_again(enemy: 'Enemy'):
        for c in enemy.components:
            c.enable()
        #enemy.state = Actor.State.Active
        enemy.stunned = False
    
    def turn_on_collision(enemy: 'Enemy'):
        enemy.collision.clear_excludes()
    
    def is_stunned(self) -> bool:
        return self.stunned
    
    def stop(self, time: float):
        self.stunned = True
        self.notify()
        for c in self.components:
            c.disable()
        #self.disable_all_components_for_time(time)
        #self.state = Actor.State.Paused
        EventManager.get_instance().add_event(Event(Enemy.start_again, time, self))
    
    def damage(self, damage: int):
        self.flash.start_flash(0.5)
        self.collision.exclude(self.game.player)
        EventManager.get_instance().add_event(Event(Enemy.turn_on_collision, 0.5, self))


class SpriteEnemy(Enemy, IActorWithSprite):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 collision: Vector2, texture: str, scale: float = 1.0, name=''):
        super().__init__(game, starting_position, collision, scale, name)
        self.texture = texture
        self.sprite = Sprite(self, 50)
        self.sprite.load_texture(texture)
    
    def set_scale(self, scale: float):
        self.scale = scale
        self.sprite.scale(scale)

class AnimatedEnemy(Enemy, IActorWithAnimated):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 anim_src: str, name=''):
        super().__init__(game, starting_position, Vector2(0, 0), 1.0, name)
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim_src)

class FixedMovingEnemy(AnimatedEnemy):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 anim_src: str, nodes: list[Node], speed: float, name=''):
        super().__init__(game, starting_position, anim_src, name)
        FollowNodes(self, nodes, speed)

class DumbChaseEnemy(AnimatedEnemy):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 anim_src: str, close_dist: float, speed: float, name=''):
        super().__init__(game, starting_position, anim_src, name)
        dc = None
        if close_dist == 0.0:
            dc = DumbChase(self, speed, False, False)
        else:
            dc = DumbChase(self, speed, True, close_dist)
        dc.set_target(game.player)