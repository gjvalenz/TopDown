from pygame import Rect
from util.math import Vector2

class AnimInfo:
    def __init__(self, col: Vector2, width_height: Vector2, still_index: int):
        self.col = col
        self.still_index = still_index
        self.width_height = width_height
        self.rects: list[Rect] = []
    
    def add_rect(self, x: int, y: int):
        self.rects.append(Rect(x, y, self.width_height.x, self.width_height.y))