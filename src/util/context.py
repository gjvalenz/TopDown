from util.save import SaveManager, Save
from actors.player import Player
from util.load_data import load_from_json_to_game

class ContextManager:
    _instance = None

    def __init__(self):
        pass

    def get_instance() -> 'ContextManager':
        if not ContextManager._instance:
            ContextManager._instance = ContextManager()
        return ContextManager._instance

    def load(self, game: 'Game'):
        save: Save = SaveManager.get_instance().save
        player_loaded: bool = load_from_json_to_game(game, f'../assets/locations/{save.location}.json')
        print(player_loaded)
        print(game.player.position)
        position = save.position
        if not player_loaded:
            print('not loaded')
            game.player = Player(game, position, '../assets/player/player_anim.json')
        if position.x != float('-inf'):
            print(f'good position: {position}')
            game.player.position = position
        game.location = save.location
        game.player.health = save.health
        game.quest = save.quest
        game.quest_index = save.quest_index
