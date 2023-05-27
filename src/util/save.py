from os import path
from util.math import Vector2
import pickle

class Save:
    def __init__(self):
        self.quest: int = 0 # which quest is the player in
        self.quest_index: int = 0 # where in the quest is the player
        self.position: Vector2 = Vector2(float('-inf'), float('-inf')) # location
        self.location: str = 'forbidden_forest'
        self.health: float = 5.0 # player health
    
    def update_save(self, game: 'Game'):
        self.health = game.player.health
        self.quest = game.quest
        self.quest_index = game.quest_index
        self.position = game.player.position
        self.location = game.location

    def save_to_file(self):
        with open('../save.dat', 'wb') as file:
            pickle.dump(self, file)
    
    def read_from_file(self):
        with open('../save.dat', 'rb') as file:
            s: Save = pickle.load(file)
            self.health = s.health
            self.quest = s.quest
            self.quest_index = s.quest_index
            self.position = s.position
            self.location = s.location

def find_save_file() -> Save:
    if path.isfile('../save.dat'): # save file exists, return it
        with open('../save.dat', 'rb') as file:
            save: Save = pickle.load(file)
            return save
    else:
        save: Save = Save()
        with open('../save.dat', 'wb') as file:
            pickle.dump(save, file)
        return save

class SaveManager:
    _instance = None

    def __init__(self):
        self.save: Save = find_save_file()

    def get_instance() -> 'SaveManager':
        if not SaveManager._instance:
            SaveManager._instance = SaveManager()
        return SaveManager._instance

    # only called upon exiting game!
    def update_save(self, game: 'Game'):
        self.save.update_save(game)
        self.save.save_to_file()
