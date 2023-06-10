from components.component import Component
from util.util import max_x, max_y
from util.interfaces import IDrawableComponent
import pygame

Surface = pygame.Surface
Font = pygame.font.Font

class Dialogue(Component, IDrawableComponent):
    def __init__(self, actor: 'Actor'):
        super().__init__(actor)
        self.actor: 'Actor' = actor
        self.texture: None|Surface = None
        self.visible: bool = True
        self.draw_order: int = 150
        self.text: str = ''
        self.font: Font = pygame.font.Font('freesansbold.ttf', 16)
        self.text_surface: None|Surface = None
        self.actor.game.add_drawable(self)
    
    def remove(self):
        self.actor.game.remove_drawable(self)
    
    def load_text(self, text: str):
        self.text = text
        self.text_surface = self.font.render(self.text, True, (0, 0, 0), None)
    
    def draw(self, screen: Surface):
        if self.text:
            w: int = max_x
            h: int = max_y / 6
            x: int = 0
            y: int = int(5.0/6.0 * max_y)
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            text_rect = self.text_surface.get_rect()
            text_rect.topleft = (x + 10, y)
            screen.blit(self.text_surface, text_rect)
