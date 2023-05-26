import pygame
from actors.actor import Actor
from components.sprite import Sprite
from util.math import Vector2

Surface = pygame.Surface

class RectFigure(Sprite):
    def __init__(self, actor: Actor, draw_order: int = 100):
        super().__init__(actor, draw_order)
        self.scale = 1.0

    def set_properties(self, width: int, height: int, color: tuple[int, int, int] = (255, 255, 255)):
        self.width = width
        self.height = height
        self.color = color
    
    def set_scale(self, scale: float):
        self.scale = scale
    
    def draw(self, screen: Surface):
        if self.color:
            dest: Vector2 = self.actor.position
            camera_pos: Vector2 = self.get_game().camera
            w, h = self.width * self.scale, self.height * self.scale
            x: int = int(dest[0] - camera_pos[0] - w/2)
            y: int = int(dest[1] - camera_pos[1] - h/2)
            rect = pygame.Rect(x, y, w, h)
            texture = Surface((w, h))
            texture.fill(self.color)
            screen.blit(texture, rect)
