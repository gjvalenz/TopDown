from abc import ABC, abstractmethod
from typing import List

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        pass
    @abstractmethod
    def detach(self, observer: 'Observer') -> None:
        pass
    def notify(self) -> None:
        pass

class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass

class EnemyInstance(Subject):
    observers: List[Observer] = []
    def attach(self, o: Observer) -> None:
        if o:
            self.observers.append(o)
    def detach(self, ob: Observer) -> None:
        self.observers = [o for o in self.observers if o != ob]
    def notify(self):
        for o in self.observers:
            o.update(self)