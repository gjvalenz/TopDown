from __future__ import annotations
import pygame
import actors.actor as actor
from actors.enemy import Enemy
#from save import Save, find_save_file
from actors.player import Player
from util.math import Vector2
from util.util import max_x, max_y
from util.load_data import load_from_json_to_game
from util.event import EventManager
from util.interfaces import IDrawableComponent

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

    def load_data(self):
        #self.save_data: Save = find_save_file()
        load_from_json_to_game(self, '../assets/levels/level1.json')
    
    def init(self):
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((max_x, max_y))
        pygame.display.set_caption('TopDown')
        self.load_data()
    
    def shutdown(self):
        pygame.quit()
        for actor in self.actors:
            actor.remove()
        self.actors = []

