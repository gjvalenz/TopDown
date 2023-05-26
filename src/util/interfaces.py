from abc import ABC
from pygame import Surface
from components.collision import Collision
from components.sprite import AnimatedSprite, Sprite

class IDrawableComponent(ABC):
    # should always have these instance attributes
    visible: bool
    actor: 'Actor'
    draw_order: int

    @classmethod
    def draw(self, screen: Surface):
        raise NotImplementedError()

class IActorWithCollision(ABC):
    collision: Collision

class IActorWithSprite(ABC):
    sprite: Sprite

class IActorWithAnimated(ABC):
    animated: AnimatedSprite
