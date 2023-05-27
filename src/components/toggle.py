from components.component import Component
from components.collision import Collision
from components.follownodes import FollowNodes
from actors.actor import Actor
from util.controls import control_pressed

class Toggle(Component):
    def __init__(self, actor: 'Actor', control_depends: list[int]):
        super().__init__(actor)
        self.control_pressed: bool = False
        self.control: list[int] = control_depends
        self.toggled: bool = False
    
    def activate_toggle(self):
        pass

    def deactivate_toggle(self):
        pass
    
    def process_input(self, keys: list[bool]):
        pressed_now: bool = control_pressed(self.control, keys)
        if not self.control_pressed and pressed_now:
            if not self.toggled:
                self.activate_toggle()
            else:
                self.deactivate_toggle()
            self.toggled = not self.toggled
        self.control_pressed = pressed_now

class DevTools(Toggle):
    def __init__(self, actor: 'Actor', control_depends: list[int]):
        super().__init__(actor, control_depends)
        self.game = self.actor.game
        self.collision = self.actor.collision
        self.cols = [self.game.enemies, self.game.colliders, self.game.npcs]
    
    def activate_toggle(self):
        for cs in self.cols:
            for c in cs:
                col: Collision = c.collision
                col.sprite_rect.visible = True
                follow_nodes: FollowNodes = c.get_component(FollowNodes)
                if follow_nodes:
                    follow_nodes.visible_nodes = True
        self.collision.sprite_rect.visible = True

    def deactivate_toggle(self):
        for cs in self.cols:
            for c in cs:
                col: Collision = c.collision
                col.sprite_rect.visible = False
                follow_nodes: FollowNodes = c.get_component(FollowNodes)
                if follow_nodes:
                    follow_nodes.visible_nodes = False
        self.collision.sprite_rect.visible = False

class TestDamage(Toggle):
    def __init__(self, actor: 'Actor', control_depends: list[int]):
        super().__init__(actor, control_depends)
        self.game = self.actor.game
    
    def activate_toggle(self):
        for c in self.game.enemies:
            c.damage(1.5)

    def deactivate_toggle(self):
        self.activate_toggle()
    


