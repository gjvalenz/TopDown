from components.sprite import Sprite
from components.approachposition import ApproachPosition

class FollowNodes(ApproachPosition):
    def __init__(self, actor: 'Actor', nodes: list['Node'], speed: float, visible_nodes: bool = False, include_player: bool = True):
        super().__init__(actor, speed, False, 0.0)
        self.nodes: list['Node'] = nodes
        self.goal_index: int = 0
        self.goal_node: None|'Node' = nodes[0]
        self.include_player: bool = include_player
        self.visible_nodes: bool = visible_nodes
    
    def update(self, dt: float):
        if self.goal_index + 1 >= len(self.nodes):
            self.nodes.reverse()
            self.goal_index = 0
            self.goal_node = self.nodes[0]
        if self.goal_node.close_enough(self.actor.position):
            self.goal_index += 1
            self.goal_node = self.nodes[self.goal_index]
        for n in self.nodes:
            if n != self.goal_node:
                n.set_scale(1.0)
            else:
                n.set_scale(3.0)
        self.set_position(self.goal_node.position)
        super().update(dt)

            

