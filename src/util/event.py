from actors.actor import Actor
from typing import Callable, Any

class Event:
    def __init__(self, func: Callable[[Actor], Any], time_from_now: float, actor: Actor):
        self.timer: float = time_from_now
        self.func = func
        self.actor = actor
    
    def tick(self, dt: float):
        self.timer -= dt
    
    def ready(self):
        return self.timer <= 0.0
    
    def apply(self):
        self.func(self.actor)


class EventManager:

    _instance = None

    def __init__(self):
        self.events: list[Event] = []
    
    def get_instance() -> 'EventManager':
        if EventManager._instance == None:
            EventManager._instance = EventManager()
        return EventManager._instance

    def add_event(self, event: Event):
        self.events.append(event)
    
    def run(self, time: float):
        for e in self.events:
            e.tick(time)
            if e.ready():
                e.apply()
        self.events = [e for e in self.events if not e.ready()]
