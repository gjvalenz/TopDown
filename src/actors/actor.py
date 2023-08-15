from __future__ import annotations
from enum import Enum
#from pygame import event
from util.event import EventManager, Event
from util.math import Vector2

#Event = event.Event

class Actor:
    State = Enum('State', ['Active', 'Destroyed', 'Paused'])
    def __init__(self, game: 'Game', name=''):
        self.state: Actor.State = Actor.State.Active
        self.components: list[Component] = []
        self.position: Vector2 = Vector2()
        self.scale: float = 1.0
        self.rotation: float = 0.0
        self.paused: bool = False
        self.game: 'Game' = game
        if name:
            self.name = name
        else:
            self.name = ''
        self.game.add_actor(self)
    
    def enable_all_components(a: 'Actor'):
        for c in a.components:
            c.enable()

    def enable_all_components_s(self):
        for c in self.components:
            c.enable()
        
    def disable_all_components_for_time(self, t: float):
        for c in self.components:
            c.disable()
        EventManager.get_instance().add_event(Event(Actor.enable_all_components, t, self))
    
    def disable_all_components(self):
        for c in self.components:
            c.disable()
    
    def remove(self):
        for component in self.components:
            component.remove()
        self.components = []
    
    def add_component(self, component: 'Component'):
        if component not in self.components:
            self.components.append(component)
            sorted(self.components, key=lambda component: component.update_order)
    
    def remove_component(self, component: 'Component'):
        component.remove()
        if component in self.components:
            self.components.remove(component)
    
    def on_update(self, dt: float): # virtual
        pass
    
    def update(self, dt: float):
        if self.state == Actor.State.Active:
            for component in self.components:
                if not component.get_disabled():
                    component.update(dt)
            self.on_update(dt)
    
    def on_process_input(self, keys: list[bool]): # virtual
        pass
    
    def process_input(self, keys: list[bool]):
        if self.state == Actor.State.Active:
            for component in self.components:
                if not component.get_disabled():
                    component.process_input(keys)
            self.on_process_input(keys)
    
    def get_component(self, Type):
        for c in self.components:
            if isinstance(c, Type):
                return c
        return None
    
    def stop(self):
        pass
