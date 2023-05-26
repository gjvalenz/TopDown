from actors.actor import Actor
from util.math import Vector2
from components.sprite import Sprite
from actors.node import Node
from components.collision import Collision
from components.animatedsprite import AnimatedSprite
from components.follownodes import FollowNodes

class NPC(Actor):
    def __init__(self, game: 'Game', startingPosition: Vector2, texture: str, scale: float = 1.0, collision: Vector2 = Vector2()):
        super().__init__(game)
        self.position = startingPosition
        self.collision = Collision(self)
        self.scale = scale
        if texture:
            self.texture = texture
            self.sprite = Sprite(self, 50)
            self.sprite.load_texture(texture)
        if collision.length() <= 0.0 and texture:
            rect = self.sprite.texture.get_rect()
            self.collision.set_size(rect.height, rect.width)
        elif collision.length() <= 0.0 and not texture:
            self.collision.set_size(0, 0)
        else:
            self.collision.set_size(collision.y, collision.x)
        game.add_npc(self)
    
    def set_scale(self, scale: float):
        self.scale = scale
        self.sprite.scale(scale)

class MovingNPC(NPC):
    def __init__(self, game: 'Game', startingPosition: Vector2, anim_src: str, nodes: list[Node], speed: float):
        super().__init__(game, startingPosition, None)
        FollowNodes(self, nodes, speed)
        for n in nodes:
            n.attach_parent(self)
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim_src)

