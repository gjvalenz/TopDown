from actors.actor import Actor
from util.math import Vector2
from components.sprite import AnimatedSprite
from components.playermove import PlayerMove
from components.collision import Collision
from components.camera import Camera
from components.dialogue import Dialogue
from components.ability import StunArea
from components.toggle import DevTools, TestDamage
from util.controls import ABILITY_3_CONTROL, TEST_DAMAGE_CONTROL, DEVTOOLS_CONTROL, INTERACT_CONTROL, control_pressed

class Player(Actor):
    def __init__(self, game: 'Game', starting_position: Vector2, anim: str, name=''):
        super().__init__(game, name)
        self.position = starting_position
        self.animated = AnimatedSprite(self, 50)
        self.animated.load_animation_info(anim)
        self.collision = Collision(self)
        self.collision.set_size(0, 0)
        self.dialogue_timer_old = 0.5
        self.dialogue_timer = 0.5 # unable to use dialogue after the fact
        self.health: float = 0.0
        self.interact_pressed_before = False
        PlayerMove(self)
        StunArea(self, ABILITY_3_CONTROL, 5.0, 0.25)
        DevTools(self, DEVTOOLS_CONTROL)
        TestDamage(self, TEST_DAMAGE_CONTROL)
        Camera(self)

    @staticmethod
    def __enable_components(a: Actor):
        for c in a.components:
            c.enable()
    
    def on_process_input(self, keys: list[bool]):
        interact_pressed_now = control_pressed(INTERACT_CONTROL, keys)
        if not self.interact_pressed_before and interact_pressed_now and self.game.talking_to == None and self.dialogue_timer < 0.0:
            for npc in self.game.npcs:
                dist = Vector2(self.position - npc.position)
                dist = dist.length()
                if dist <= 45.0:
                    self.game.talking_to = npc
                    self.disable_all_components()
                    npc.disable_all_components()
                    if npc.name == 'Watermelon Wizard':
                        d = Dialogue(self, -1)
                        d.load_text('Hello there young Wizard...')
                    elif npc.name == 'Old Man John':
                        d = Dialogue(self, -1)
                        d.load_text("These days, I'm as old as old Watermelon Wizard...")                    
                    #print(f'talked to {npc.name}')
        self.interact_pressed_before = interact_pressed_now
        pass
    
    def on_update(self, dt: float):
        self.dialogue_timer -= dt
        pass