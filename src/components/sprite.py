import pygame
from actors.actor import Actor
from components.component import Component
from util.math import Vector2

Surface = pygame.Surface

class Sprite(Component):
    def __init__(self, actor: Actor, draw_order: int = 100):
        super().__init__(actor)
        self.actor: Actor = actor
        self.texture: None|Surface = None
        self.visible: bool = True
        self.draw_order: int = draw_order
        self.actor.game.add_sprite(self)
    
    def remove(self):
        self.actor.game.remove_sprite(self)
    
    def load_texture(self, texture_loc: str):
        self.true_texture = pygame.image.load(texture_loc)
        self.true_width = self.true_texture.get_width()
        self.true_height = self.true_texture.get_height()
        scale = self.actor.scale
        self.texture = pygame.transform.scale(self.true_texture, (self.true_width * scale, self.true_height * scale))
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
    
    def scale(self, scale: float = 1.0):
        self.texture = pygame.transform.scale(self.true_texture, (self.true_width * scale, self.true_height * scale))
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
    
    
    def draw(self, screen: Surface):
        if self.texture:
            dest: Vector2 = self.actor.position
            camera_pos: Vector2 = self.get_game().camera
            w, h = self.width, self.height
            x: int = int(dest[0] - camera_pos[0] - w/2)
            y: int = int(dest[1] - camera_pos[1] - h/2)
            rect = pygame.Rect(x, y, w, h)
            screen.blit(self.texture, rect)