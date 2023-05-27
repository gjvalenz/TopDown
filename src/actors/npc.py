from actors.actor import Actor
from util.math import Vector2
from components.sprite import Sprite, AnimatedSprite
from actors.node import Node
from components.collision import Collision
from components.follownodes import FollowNodes
from util.interfaces import IActorWithCollision, IActorWithAnimated, IActorWithSprite

class NPC(Actor, IActorWithCollision):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 collision: Vector2, scale: float = 1.0):
        super().__init__(game)
        self.position = starting_position
        self.scale = scale
        self.collision = Collision(self)
        self.collision.set_size(collision.y * self.scale, collision.x * self.scale)
        game.add_npc(self)

class SpriteNPC(NPC, IActorWithSprite):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 collision: Vector2, texture: str, scale: float = 1.0, ):
        super().__init__(game, starting_position, collision, scale)
        self.texture = texture
        self.sprite = Sprite(self, 50)
        self.sprite.load_texture(texture)
    
    def set_scale(self, scale: float):
        self.scale = scale
        self.sprite.scale(scale)

class AnimatedNPC(NPC, IActorWithAnimated):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 anim_src: str):
        super().__init__(game, starting_position, Vector2(0, 0), 1.0)
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim_src)

class MovingNPC(AnimatedNPC):
    def __init__(self, game: 'Game', starting_position: Vector2,
                 anim_src: str, nodes: list[Node], speed: float):
        super().__init__(game, starting_position, anim_src)
        FollowNodes(self, nodes, speed)

