from actors.actor import Actor
from actors.node import Node
from actors.npc import SpriteNPC, MovingNPC
from components.sprite import Sprite
from actors.player import Player
from actors.collider import Collider, ImgCollider
from actors.enemy import FixedMovingEnemy, DumbChaseEnemy
from util.math import Vector2
from util.util import vector2_from_json, str_from_json, float_from_json
from util.audio import Audio
from json import load

def load_from_json_to_game(game: 'Game', filename: str) -> bool:
    loaded_player: bool = False
    with open(filename, 'r') as file:
        data = load(file)
        for buildable in data['buildables']:
            if buildable['type'] == 'Player':
                player = buildable
                position = vector2_from_json(player, 'position')
                anim = player['animation']
                game.player = Player(game, position, anim)
                loaded_player = True
            if buildable['type'] == 'Collider':
                collider = buildable
                position = vector2_from_json(collider, 'position')
                dimensions = vector2_from_json(collider, 'dimensions')
                col = Collider(game, position, Vector2(dimensions[0], dimensions[1]))
            if buildable['type'] == 'ImgCollider':
                collider = buildable
                position = vector2_from_json(collider, 'position')
                txt = str_from_json(collider, 'texture')
                scale = float_from_json(collider, 'scale', 1.0)
                collision = vector2_from_json(collider, 'col')
                col = ImgCollider(game, position, txt, collision, scale)
            if buildable['type'] == 'NPC':
                npc = buildable
                position = vector2_from_json(npc, 'position')
                txt = str_from_json(npc, 'texture')
                scale = float_from_json(npc, 'scale', 1.0)
                collision = vector2_from_json(npc, 'col')
                npc = SpriteNPC(game, position, collision, txt, scale)
            if buildable['type'] == 'MovingNPC':
                npc = buildable
                position = vector2_from_json(npc, 'position')
                anim = npc['animation']
                speed = float_from_json(npc, 'speed')
                positions: list[list] = npc['nodes']
                accurate_positions: list[Vector2] = []
                for n in positions:
                    accurate_positions.append(Vector2(n[0], n[1]))
                nodes: list[Node] = []
                for p in accurate_positions:
                    nodes.append(Node(game, p))
                moving_npc = MovingNPC(game, position, anim, nodes, speed)
            if buildable['type'] == 'FixedMovingEnemy':
                enemy = buildable
                position = vector2_from_json(enemy, 'position')
                anim = enemy['animation']
                speed = float_from_json(enemy, 'speed')
                positions: list[list] = enemy['nodes']
                accurate_positions: list[Vector2] = []
                for n in positions:
                    accurate_positions.append(Vector2(n[0], n[1]))
                nodes: list[Node] = []
                for p in accurate_positions:
                    nodes.append(Node(game, p))
                moving_enemy = FixedMovingEnemy(game, position, anim, nodes, speed)
            if buildable['type'] == 'PlayerChaserEnemy':
                enemy = buildable
                position = vector2_from_json(enemy, 'position')
                anim = enemy['animation']
                speed = float_from_json(enemy, 'speed')
                close_stop = float_from_json(enemy, 'close_stop')
                scale = float_from_json(enemy, 'scale', 1.0)
                chasing_enemy = DumbChaseEnemy(game, position, anim, close_stop, speed)
                chasing_enemy.scale = scale
        game.map = Actor(game)
        map_background = Sprite(game.map, 10)
        map_data = data['map']
        map_background.load_texture(map_data['texture'])
        rect = map_background.texture.get_rect()
        game.map_dim = Vector2(rect.width, rect.height)/2
        if 'sounds' in data:
            for song_data in data['sounds']:
                Audio.get_instance().play_song(song_data['name'], song_data['location'], song_data['looping'])
    return loaded_player