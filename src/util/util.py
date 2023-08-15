from util.math import Vector2

max_x: int = 600
max_y: int = max_x

def vector2_from_json(json_struct, attr_name: str, default_value: Vector2 = Vector2()) -> Vector2:
    if attr_name in json_struct:
        return Vector2(json_struct[attr_name][0], json_struct[attr_name][1])
    else:
        return default_value

def str_from_json(json_struct, attr_name: str, default_value: str = str()) -> str:
    if attr_name in json_struct:
        return json_struct[attr_name]
    else:
        return default_value

def list_from_json(json_struct, attr_name: str, default_value: list = []) -> list:
    if attr_name in json_struct:
        return json_struct[attr_name]
    else:
        return default_value

def float_from_json(json_struct, attr_name: str, default_value: float = 0.0) -> float:
    if attr_name in json_struct:
        return json_struct[attr_name]
    else:
        return default_value

def bool_from_json(json_struct, attr_name: str, default_value: bool = False) -> bool:
    if attr_name in json_struct:
        return json_struct[attr_name]
    else:
        return default_value