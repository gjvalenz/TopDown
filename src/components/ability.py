from components.component import Component
from actors.collider import Collider
from actors.actor import Actor
from components.playermove import PlayerMove
from util.math import Vector2
from util.controls import control_pressed

class Ability(Component):
    def __init__(self, actor: 'Actor', control_depends: list[int],
                 cooldown: float, t_alive: float, starting_cd: float = 0.0):
        super().__init__(actor)
        self.control_pressed: bool = False
        self.control: list[int] = control_depends
        self.max_cd: float = cooldown
        self.max_t_alive: float = t_alive
        self.cd: float = starting_cd
        self.t_alive: float = 0.0
        self.ability_active: bool = False
        self.enabled: bool = True
    
    def activate_ability(self):
        pass

    def deactivate_ability(self):
        pass

    def ability_effect(self):
        pass
    
    def process_input(self, keys: list[bool]):
        if not self.enabled:
            return
        pressed_now: bool = control_pressed(self.control, keys)
        if not self.control_pressed and pressed_now:
            self.activate_ability()
            self.cd = self.max_cd
            self.t_alive = self.max_t_alive
            self.ability_active = True
        self.control_pressed = pressed_now
    
    def update(self, dt: float):
        if self.cd > 0.0:
            self.cd = max(0.0, self.cd - dt)
        if self.ability_active:
            self.t_alive = max(0.0, self.t_alive - dt)
            if self.t_alive <= 0.0:
                self.ability_active = False
                self.deactivate_ability()
                return
            self.ability_effect()

class StunArea(Ability):
    def __init__(self, actor: 'Actor', control_depends: list[int],
                 cooldown: float, t_alive: float, starting_cd: float = 0.0):
        super().__init__(actor, control_depends, cooldown, t_alive, starting_cd)
        self.area: None|Collider = None
    
    def activate_ability(self):
        move = self.actor.get_component(PlayerMove)
        direction = move.get_direction()
        big_dim: int = 200
        small_dim: int = 200
        offset = big_dim/2 + 20
        width: int = 0
        height: int = 0
        offset_from_player: Vector2 = Vector2()
        if direction == PlayerMove.Direction.RIGHT or direction == PlayerMove.Direction.LEFT:
            width = big_dim
            height = small_dim
            polarity = 1 if direction == PlayerMove.Direction.RIGHT else -1
            offset_from_player = Vector2(polarity * offset, 0)
        if direction == PlayerMove.Direction.DOWN or direction == PlayerMove.Direction.UP:
            width = small_dim
            height = big_dim
            polarity = 1 if direction == PlayerMove.Direction.DOWN else -1
            offset_from_player = Vector2(0, polarity * offset)
        self.area = Collider(self.actor.game, self.actor.position + offset_from_player, Vector2(width, height), 1.0, (0, 0, 255))
        self.area.figure.visible = True

    def deactivate_ability(self):
        self.area.state = Actor.State.Destroyed

    def ability_effect(self):
        for c in self.actor.game.enemies:
            if self.area.collision.intersect(c.collision):
                if not c.is_stunned():
                    c.stop(2)

