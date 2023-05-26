from abc import ABC
from pygame import Surface

class IDrawableComponent(ABC):
    # should always have these instance attributes
    visible: bool
    actor: 'Actor'
    draw_order: int

    @classmethod
    def draw(self, screen: Surface):
        raise NotImplementedError()

class IActorWithCollision(ABC):
    collision: 'Collision'

class IActorWithSprite(ABC):
    sprite: 'Sprite'

class IActorWithAnimated(ABC):
    animated: 'AnimatedSprite'
