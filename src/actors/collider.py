from actors.actor import Actor
from util.math import Vector2
from components.collision import Collision
from components.sprite import Sprite
from components.rectfigure import RectFigure

class Collider(Actor):
    def __init__(self, game: 'Game', position: Vector2, width: int, height: int, scale: float = 1.0, figure_text: bool = False, figure_text_color: tuple[int, int, int] = (0, 255, 0)):
        super().__init__(game)
        if figure_text:
            figure = RectFigure(self)
            figure.set_properties(width, height, figure_text_color)
        self.position = position
        self.scale = scale
        self.collision = Collision(self)
        self.collision.set_size(height, width)
        game.add_collider(self)
    
    def remove(self):
        self.game.remove_collider(self)
        super().remove()
    


class ImgCollider(Collider):
    def __init__(self, game: 'Game', position: Vector2, texture: str, scale: float = 1.0, collision: Vector2 = Vector2()):
        super().__init__(game, position, 0, 0, scale)
        self.sprite = Sprite(self)
        self.sprite.load_texture(texture)
        if collision.length() <= 0.0:
            sprite_width = self.sprite.texture.get_width()
            sprite_height = self.sprite.texture.get_height()
            self.collision.set_size(sprite_height, sprite_width)
        else:
            self.collision.set_size(collision.y, collision.x)
    
    def set_scale(self, scale: float):
        self.scale = scale
        self.sprite.scale(scale)
