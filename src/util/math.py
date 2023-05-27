from pygame import math

Vector2 = math.Vector2

def clamp(min: int, value: int, max: int) -> int:
    return sorted([min, value, max])[1] # always returns middle value