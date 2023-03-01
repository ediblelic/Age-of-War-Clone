import pygame
from pygame.image import load 
from settings import WARRIOR_PATH as warrior
from settings import ARCHER_PATH as archer
import dataclasses
@dataclasses.dataclass
class Status:
    cost: int
    health: int
    demage: int
    move_speed: int
    animation_time : int
    movement: bool
    attack: bool
class SwordMan(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        #LOADING SPRITES
        self.load_sprites()
        self.image = self.sword_man_walking[self.current_sword_man_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))
        #SWORDMAN STATUS
        self.sword_man_status = Status(15,300,2,80,8,True,False)
        self.vector_direction = pygame.math.Vector2(self.rect.topleft)
    def load_sprites(self):
        self.sword_man_walking = []
        self.sword_man_attack = []
        self.display_surface = pygame.display.get_surface()
        #LOADING SPRITES
        for img in range(10):
            self.sword_man_walking.append(
            load(f"{warrior}walking/warrior{img}.png").convert_alpha()
                                        )
        for img in range(11):
            self.sword_man_attack.append(load
            (f"{warrior}attacking/attack{img}.png").convert_alpha()
                                        )
        self.current_sword_man_sprite = 0
        self.attack_animation_sprite = 0
    def walking_animation(self,dt):
        if self.sword_man_status.movement:
            self.current_sword_man_sprite += (self.sword_man_status.animation_time * dt)
            if self.current_sword_man_sprite >= len(self.sword_man_walking):
                self.current_sword_man_sprite = 0
    def attacking_animations(self,dt,enemy):
        self.sword_man_status.attack = True
        self.sword_man_status.movement = False
        if self.sword_man_status.attack:
            self.attack_animation_sprite += (self.sword_man_status.animation_time * dt)
            if self.attack_animation_sprite >= len(self.sword_man_attack):
                self.attack_animation_sprite = 0
            if enemy == -1:
                self.image = pygame.transform.flip(self.sword_man_attack[int(self.attack_animation_sprite)],True,False)
            else:
                self.image = self.sword_man_attack[int(self.attack_animation_sprite)]
            
    def movement(self,dt,enemy):
        prev_x = self.vector_direction.x
        if self.sword_man_status.movement:
            self.vector_direction.x += (self.sword_man_status.move_speed * dt) * enemy
            self.rect.x = round(self.vector_direction.x)
        if self.vector_direction.x <= prev_x and enemy == -1:
            self.image = pygame.transform.flip(self.sword_man_walking[int(self.current_sword_man_sprite)], True, False)
        else:
            self.image = self.sword_man_walking[int(self.current_sword_man_sprite)]
    def stop_movement(self):
        self.sword_man_status.movement = False
    def attack(self,dt,enemy):
        self.attacking_animations(dt,enemy)
    def update(self,dt,enemy):
        self.movement(dt,enemy)
        self.walking_animation(dt)

class Archer(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        #Loading sprites
        self.load_sprites()
        self.image = self.archer_walking[self.index_walking_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))
        #ARCHMAN STATUS
        self.archer_status = Status(35,50,4,75,12,True,False)
        self.vector_direction = pygame.math.Vector2(self.rect.topleft)
    def load_sprites(self):
        self.display_surface = pygame.display.get_surface()
        self.archer_walking = []
        self.archer_attack = []
        for walk in range(10):
            self.archer_walking.append(load
                (f"{archer}walk/player_walk{walk}.png").convert_alpha()
                )
        for attack in range(10):
            self.archer_attack.append(load
                (f"{archer}attack/attack{attack}.png").convert_alpha()
                )
        self.index_walking_sprite = 0
        self.index_attacking_sprite = 0
    def walking_animation(self,dt):
        if self.archer_status.movement:
            self.index_walking_sprite += (self.archer_status.animation_time * dt)
            if self.index_walking_sprite >= len(self.archer_walking):
                self.index_walking_sprite = 0
    def attacking_animations(self,dt):
        self.archer_status.attack = True
        self.archer_status.movement = False
        if self.archer_status.attack:
            self.index_attacking_sprite += (self.archer_status.animation_time * dt)
            if self.index_attacking_sprite >= len(self.archer_attack):
                self.index_attacking_sprite = 0
            self.image = self.archer_attack[int(self.index_attacking_sprite)]
    def movement(self,dt,enemy):
        prev_x = self.vector_direction.x
        if self.archer_status.movement:
            self.vector_direction.x += (self.archer_status.move_speed * dt) * enemy
            self.rect.x = round(self.vector_direction.x)
        if self.vector_direction.x < prev_x:
            self.image = pygame.transform.flip(self.archer_walking[int(self.index_walking_sprite)], True, False)
        else:
            self.image = self.archer_walking[int(self.index_walking_sprite)]
    def stop_movement(self):
        self.archer_status.movement = False
    def attack(self,dt):
        self.attacking_animations(dt)
    def update(self,dt,enemy):
        self.movement(dt,enemy)
        self.walking_animation(dt)
class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass
