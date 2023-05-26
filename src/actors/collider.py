from actors.actor import Actor
from util.math import Vector2
from components.collision import Collision
from components.sprite import Sprite
from components.rectfigure import RectFigure

class Collider(Actor):
    def __init__(self, game: 'Game', position: Vector2,
                 width_height: Vector2, scale: float = 1.0,
                 figure_text_color: tuple[int, int, int] = (0, 255, 0)):
        super().__init__(game)
        self.figure = RectFigure(self)
        self.figure.set_properties(width_height.x, width_height.x, figure_text_color)
        self.figure.visible = False
        self.position = position
        self.scale = scale
        self.collision = Collision(self)
        self.collision.set_size(width_height.y * self.scale, width_height.x * self.scale)
        game.add_collider(self)
    
    def remove(self):
        self.game.remove_collider(self)
        super().remove()
    
    def toggle_show(self):
        self.figure.visible = not self.figure.visible


class ImgCollider(Collider):
    def __init__(self, game: 'Game', position: Vector2, texture: str,
                 collision: Vector2, scale: float = 1.0):
        super().__init__(game, position, collision, scale)
        self.sprite = Sprite(self)
        self.sprite.load_texture(texture)
        #self.collision.set_size(collision.y, collision.x)
    
    def set_scale(self, scale: float):
        self.scale = scale
        self.sprite.scale(scale)
