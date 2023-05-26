import pygame
from actors.actor import Actor
from components.component import Component
from util.interfaces import IDrawableComponent
from util.math import Vector2
from json import load
from util.animinfo import AnimInfo

Surface = pygame.Surface
Rect = pygame.Rect

class Sprite(Component, IDrawableComponent):
    def __init__(self, actor: Actor, draw_order: int = 100):
        super().__init__(actor)
        self.actor: Actor = actor
        self.texture: None|Surface = None
        self.visible: bool = True
        self.draw_order: int = draw_order
        self.actor.game.add_drawable(self)
    
    def remove(self):
        self.actor.game.remove_drawable(self)
    
    def load_texture(self, texture_loc: str):
        self.true_texture = pygame.image.load(texture_loc)
        self.true_width = self.true_texture.get_width()
        self.true_height = self.true_texture.get_height()
        scale = self.actor.scale
        self.texture = pygame.transform.scale(self.true_texture, (self.true_width * scale, self.true_height * scale))
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
    
    def scale(self, scale: float = 1.0):
        self.texture = pygame.transform.scale(self.true_texture, (self.true_width * scale, self.true_height * scale))
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
    
    def draw(self, screen: Surface):
        if self.texture:
            dest: Vector2 = self.actor.position
            camera_pos: Vector2 = self.get_game().camera
            w, h = self.width, self.height
            x: int = int(dest[0] - camera_pos[0] - w/2)
            y: int = int(dest[1] - camera_pos[1] - h/2)
            rect = pygame.Rect(x, y, w, h)
            screen.blit(self.texture, rect)


class AnimatedSprite(Component, IDrawableComponent):
    def __init__(self, actor: Actor, draw_order: int = 100):
        super().__init__(actor)
        self.actor: Actor = actor
        self.texture: None|Surface = None
        self.visible: bool = True
        self.draw_order: int = draw_order
        self.animation_infos: dict[str, AnimInfo] = {}
        self.sub_texture: Surface = None
        self.still: bool = False
        self.curr_name: str = None
        self.anim_timer: float = 0.0
        self.anim_fps: int = 10
        self.actor.game.add_drawable(self)
    
    def remove(self):
        self.actor.game.remove_drawable(self)
    
    def load_animation_info(self, anim_info: str):
        with open(anim_info, 'r') as file:
            data = load(file)
            self.texture = pygame.image.load(data['asset'])
            for anim_info in data['animations']:
                name = anim_info['name']
                still_index = anim_info['still']
                y = anim_info['y']
                wh = anim_info['dimensions']
                wh = Vector2(wh[0], wh[1])
                col_dim = anim_info['col']
                col_dim = Vector2(col_dim[0], col_dim[1])
                self.animation_infos[name] = AnimInfo(col_dim, wh, still_index)
                for x in anim_info['x']:
                    self.animation_infos[name].add_rect(x, y)

    def get_col_dim(self):
        if self.curr_name:
            return self.animation_infos[self.curr_name].col * self.actor.scale
        return None
    
    def set_animation(self, name: str, still: bool = False):
        if self.curr_name != name or still != self.still:
            self.curr_name = name
            self.still = still
            self.anim_timer = 0.0
            a_info = self.animation_infos[self.curr_name]
            if not self.still:
                self.sub_texture = self.texture.subsurface(a_info.rects[0])
            else:
                self.sub_texture = self.texture.subsurface(a_info.rects[a_info.still_index])

    
    def update(self, dt: float):            
        if not self.curr_name or self.still:
            return
        self.anim_timer += dt * self.anim_fps
        a_info = self.animation_infos[self.curr_name]
        sz = float(len(a_info.rects))
        while self.anim_timer >= sz:
            self.anim_timer -= sz
        self.sub_texture = self.texture.subsurface(a_info.rects[int(self.anim_timer)])
    
    def draw(self, screen: Surface):
        if self.sub_texture:
            a_info = self.animation_infos[self.curr_name]
            dest: Vector2 = self.actor.position
            camera_pos: Vector2 = self.get_game().camera
            w, h = a_info.width_height.x * self.actor.scale, a_info.width_height.y * self.actor.scale
            x: int = int(dest[0] - camera_pos[0] - w/2)
            y: int = int(dest[1] - camera_pos[1] - h/2)
            rect = pygame.Rect(x, y, w, h)
            texture = pygame.transform.scale(self.sub_texture, (w, h))
            screen.blit(texture, rect)