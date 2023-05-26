from __future__ import annotations
import pygame
import actors.actor as actor
from actors.node import Node
from actors.npc import MovingNPC
from actors.enemy import FixedMovingEnemy, DumbChaseEnemy
#from save import Save, find_save_file
from components.sprite import Sprite
from actors.player import Player
from actors.npc import NPC
from actors.enemy import Enemy
from actors.collider import Collider, ImgCollider
from util.math import Vector2
from util.util import vector2_from_json, str_from_json, float_from_json, max_x, max_y
from util.event import EventManager
from util.audio import Audio
from util.interfaces import IDrawableComponent
from json import load

Event = pygame.event.Event
Clock = pygame.time.Clock
Surface = pygame.Surface
Actor = actor.Actor

class Game:
    def __init__(self):
        self.actors: list[Actor] = []
        self.running: bool = True
        self.clock: Clock = Clock()
        self.fps: int = 60
        self.sprites: list[IDrawableComponent] = []
        self.colliders: list[Actor] = []
        self.npcs: list[NPC] = []
        self.enemies: list[Enemy] = []
        self.camera: Vector2 = Vector2()
        self.player: None | Player = None
    
    def add_actor(self, actor: Actor):
        if actor not in self.actors:
            self.actors.append(actor)
    
    def remove_actor(self, actor: Actor):
        if actor in self.actors:
            self.actors.remove(actor)
    
    def add_collider(self, collider: Actor):
        if collider not in self.colliders:
            self.colliders.append(collider)
        
    def remove_collider(self, collider: Actor):
        if collider in self.colliders:
            self.colliders.remove(collider)
    
    def add_enemy(self, enemy: Enemy):
        if enemy not in self.enemies:
            self.enemies.append(enemy)
        
    def remove_enemy(self, enemy: Enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def add_npc(self, npc: NPC):
        if npc not in self.npcs:
            self.npcs.append(npc)
        
    def remove_npc(self, npc: NPC):
        if npc in self.npc:
            self.npc.remove(npc)

    def add_drawable(self, drawable: IDrawableComponent):
        if drawable not in self.sprites:
            self.sprites.append(drawable)
            self.sprites = sorted(self.sprites, key=lambda sprite: sprite.draw_order)
    
    def remove_drawable(self, drawable: IDrawableComponent):
        if drawable in self.sprites:
            self.sprites.remove(drawable)
    
    def loop(self):
        while self.running:
            self.process_input()
            self.update_game()
            self.generate_output()
    
    def process_input(self):
        keys: list[bool] = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        for actor in self.actors:
            actor.process_input(keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update_game(self):
        ms: int = self.clock.tick(self.fps)
        dt: float = ms * 0.001
        if dt >= (1.0/self.fps):
            dt = (1.0/self.fps)
        # audio update
        # event updates first
        EventManager.get_instance().run(dt)
        for actor in self.actors:
            actor.update(dt)
        for actor in self.actors:
            if actor.state == Actor.State.Destroyed:
                actor.remove()
        self.actors = [actor for actor in self.actors if actor.state != Actor.State.Destroyed]
            
    def generate_output(self):
        self.screen.fill((0, 0, 0))
        for sprite in self.sprites:
            if sprite.visible:
                sprite.draw(self.screen)
        pygame.display.update()
    
    def load_from_json(self, fn: str):
        with open(fn, 'r') as file:
            data = load(file)
            for buildable in data['buildables']:
                if buildable['type'] == 'Player':
                    player = buildable
                    position = vector2_from_json(player, 'position')
                    anim = player['animation']
                    self.player = Player(self, position, anim)
                if buildable['type'] == 'Collider':
                    collider = buildable
                    position = vector2_from_json(collider, 'position')
                    dimensions = vector2_from_json(collider, 'dimensions')
                    col = Collider(self, position, dimensions[0], dimensions[1], True)
                if buildable['type'] == 'ImgCollider':
                    collider = buildable
                    position = vector2_from_json(collider, 'position')
                    txt = str_from_json(collider, 'texture')
                    scale = float_from_json(collider, 'scale', 1.0)
                    collision = vector2_from_json(collider, 'col')
                    col = ImgCollider(self, position, txt, scale, collision)
                if buildable['type'] == 'NPC':
                    npc = buildable
                    position = vector2_from_json(npc, 'position')
                    txt = str_from_json(npc, 'texture')
                    scale = float_from_json(npc, 'scale', 1.0)
                    collision = vector2_from_json(npc, 'col')
                    npc = NPC(self, position, txt, scale, collision)
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
                        nodes.append(Node(self, p))
                    moving_npc = MovingNPC(self, position, anim, nodes, speed)
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
                        nodes.append(Node(self, p))
                    moving_enemy = FixedMovingEnemy(self, position, anim, nodes, speed)
                if buildable['type'] == 'PlayerChaserEnemy':
                    enemy = buildable
                    position = vector2_from_json(enemy, 'position')
                    anim = enemy['animation']
                    speed = float_from_json(enemy, 'speed')
                    close_stop = float_from_json(enemy, 'close_stop')
                    scale = float_from_json(enemy, 'scale', 1.0)
                    chasing_enemy = DumbChaseEnemy(self, position, anim, close_stop, speed)
                    chasing_enemy.scale = scale
            map_actor = Actor(self)
            map_background = Sprite(map_actor, 10)
            map_data = data['map']
            map_background.load_texture(map_data['texture'])
            if 'sounds' in data:
                for song_data in data['sounds']:
                    Audio.get_instance().play_song(song_data['name'], song_data['location'], song_data['looping'])


    def load_data(self):
        #self.save_data: Save = find_save_file()
        self.load_from_json('../assets/levels/level1.json')
    
    def init(self):
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((max_x, max_y))
        self.load_data()
    
    def shutdown(self):
        pygame.quit()
        for actor in self.actors:
            actor.remove()
        self.actors = []

