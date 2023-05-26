from os import path
import pickle

class Save:
    def __init__(self):
        self.checkpoint: int = 0
    
    def get_checkpoint(self) -> int:
        return self.checkpoint
    

def find_save_file() -> Save:
    if path.isfile('save.dat'): # save file exists, return it
        with open('save.dat', 'rb') as file:
            save: Save = pickle.load(file)
            return save
    else:
        save: Save = Save()
        with open('save.dat', 'wb') as file:
            pickle.dump(save, file)
        return save
    
