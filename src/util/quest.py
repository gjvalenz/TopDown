from typing import List
from util.observer import Observer, EnemyInstance
from actors.actor import Actor

class Quest:
    method: str
    count: int
    affects: str # name of thing affected
    def __init__(self, m: str, c: int, a: str):
        self.method = m
        self.count = c
        self.affects = a
    

class QuestManager(Observer):
    __instance = None
    count = 0
    quests: List[Quest] = []
    def __init__(self):
        pass
    def get_instance() -> 'QuestManager':
        if not QuestManager.__instance:
            QuestManager.__instance = QuestManager()
        else:
            return QuestManager.__instance
    def update(self, enemy: EnemyInstance):
        if enemy.is_stunned():
            self.count += 1
            print(f'{enemy.name} PAUSED!! {self.count}')
