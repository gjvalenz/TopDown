from __future__ import annotations
from pygame import event

Event = event.Event

class Component:
    def __init__(self, actor: 'Actor', update_order: int = 100):
        self.actor: 'Actor' = actor
        self.update_order: int = update_order
        self.actor.add_component(self)
        self.disabled = False

    def disable(self):
        self.disabled = True
    
    def enable(self):
        self.disabled = False

    def get_disabled(self):
        return self.disabled
    
    def get_game(self):
        return self.actor.game
    
    def update(self, dt: float):
        pass
    
    def process_input(self, keys: list[bool]):
        pass
    
    def remove(self):
        pass
