from pygame import math

Vector2 = math.Vector2

def clamp(min: float, value: float, max: float) -> float:
    return sorted([min, value, max])[1] # always returns middle value