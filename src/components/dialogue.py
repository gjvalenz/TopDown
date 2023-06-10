from components.component import Component
from util.util import max_x, max_y
from util.interfaces import IDrawableComponent
import pygame

Surface = pygame.Surface
Font = pygame.font.Font

class Dialogue(Component, IDrawableComponent):
    def __init__(self, actor: 'Actor', time_span = 0.0):
        super().__init__(actor)
        self.actor: 'Actor' = actor
        self.texture: None|Surface = None
        self.visible: bool = True
        self.draw_order: int = 150
        self.text: str = ''
        self.font: Font = pygame.font.Font('../assets/fonts/vcr_osd_mono.ttf', 22)
        self.text_surface: None|Surface = None
        self.is_timed: bool = time_span > 0.0
        self.timer: float = time_span
        self.actor.game.add_drawable(self)
    
    def remove(self):
        self.actor.game.remove_drawable(self)
    
    def load_text(self, text: str):
        self.text = text
        self.text_surface = self.font.render(self.text, True, (0, 0, 0), None)

    def update(self, dt: float):
        super().update(dt)
        if self.is_timed:
            self.timer -= dt
            if self.timer <= 0.0:
                self.remove()
                self.actor.remove_component(self)
    
    def draw(self, screen: Surface):
        if self.text:
            border_size = 4
            highlight = 30
            border_color = (highlight, highlight, highlight)
            w: int = max_x
            h: int = (max_y / 6)
            x: int = 0
            y: int = int(5.0/6.0 * max_y)
            border = pygame.Rect(x, y, w, h)
            rect = pygame.Rect(x + border_size, y + border_size, w - border_size * 2, h - border_size * 2)
            pygame.draw.rect(screen, border_color, border)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            text_rect = self.text_surface.get_rect()
            text_rect.topleft = (x + 10, y + 10)
            screen.blit(self.text_surface, text_rect)
