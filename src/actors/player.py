from actors.actor import Actor
from util.math import Vector2
from components.sprite import AnimatedSprite
from components.playermove import PlayerMove
from components.collision import Collision
from components.camera import Camera
from components.ability import StunArea
from components.toggle import DevTools, TestDamage
from util.controls import ABILITY_3_CONTROL, TEST_DAMAGE_CONTROL, DEVTOOLS_CONTROL

class Player(Actor):
    def __init__(self, game: 'Game', starting_position: Vector2, anim: str):
        super().__init__(game)
        self.position = starting_position
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim)
        self.collision = Collision(self)
        self.collision.set_size(0, 0)
        PlayerMove(self)
        StunArea(self, ABILITY_3_CONTROL, 5.0, 0.25)
        DevTools(self, DEVTOOLS_CONTROL)
        TestDamage(self, TEST_DAMAGE_CONTROL)
        Camera(self)
    
    def on_process_input(self, keys: list[bool]):
        pass
    
    def on_update(self, dt: float):
        pass