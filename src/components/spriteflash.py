from components.component import Component
from components.animatedsprite import AnimatedSprite
from components.sprite import Sprite

class SpriteFlash(Component):
    def __init__(self, actor: 'Actor', tick: int = 4):
        super().__init__(actor)
        self.flashing: bool = False
        self.flash_timer: float = 0.0
        self.flash_tick: int = 0
        self.invisible_tick: int = tick
    
    def start_flash(self, time: float):
        self.flash_timer = time
        self.flashing = True
    
    def check_flashing(self) -> bool:
        return self.flashing
    
    def update(self, dt: float):
        if self.flashing:
            self.flash_tick += 1
            self.flash_timer -= dt
            pref = self.actor.get_component(AnimatedSprite)
            if not pref:
                pref = self.actor.get_component(Sprite)
            pref.visible = self.flash_tick % self.invisible_tick != 0
            if self.flash_timer <= 0.0:
                pref.visible = True
                self.flash_timer = 0.0
                self.flash_tick = 0
                self.flashing = False

            

