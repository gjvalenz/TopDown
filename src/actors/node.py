from actors.actor import Actor
from util.math import Vector2
from components.rectfigure import RectFigure
from components.follownodes import FollowNodes

class Node(Actor):
    THRESHOLD: float = 10.0
    def __init__(self, game: 'Game', position: Vector2):
        super().__init__(game)
        self.parent: Actor = None
        self.position = position
        self.figure = RectFigure(self, 50)
        self.figure.set_properties(5, 5, (0, 255, 0))
    
    def attach_parent(self, parent: Actor):
        self.parent = parent
    
    def set_scale(self, scale: float):
        self.scale = scale
        self.figure.set_scale(scale)
    
    def distance_from(self, position: Vector2) -> float:
        return (self.position - position).length()
    
    def close_enough(self, position: Vector2) -> bool:
        return self.distance_from(position) <= Node.THRESHOLD
    
    def unit_velocity_towards(self, position: Vector2) -> Vector2:
        return (self.position - position).normalize()
    
    def update(self, dt: float):
        follow_node = self.parent.get_component(FollowNodes)
        node_sprite = self.get_component(RectFigure)
        if follow_node.visible_nodes != node_sprite.visible:
            node_sprite.visible = follow_node.visible_nodes