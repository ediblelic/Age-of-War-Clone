import pygame
from pygame.image import load 
from settings import WARRIOR_PATH as warrior
from settings import ARCHER_PATH as archer
class SwordMan(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
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
        self.image = self.sword_man_walking[self.current_sword_man_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))
        #SWORDMAN STATUS
        self.cost = 15
        self.health = 30
        self.demage = 2
        self.move_speed = 30
        self.animations_time = 4
        self.vector_direction = pygame.math.Vector2(self.rect.topleft)
        # MOVEMENT
        self.movement_status = True
        self.attack_status = False
    def walking_animation(self,dt):
        if self.movement_status:
            self.current_sword_man_sprite += (self.animations_time * dt)
            if self.current_sword_man_sprite >= len(self.sword_man_walking):
                self.current_sword_man_sprite = 0
            self.image = self.sword_man_walking[int(self.current_sword_man_sprite)]
    def attacking_animations(self,dt):
        self.attack_status = True
        self.movement_status = False
        if self.attack_status:
            self.attack_animation_sprite += (self.animations_time * dt)
            if self.attack_animation_sprite >= len(self.sword_man_attack):
                self.attack_animation_sprite = 0
            self.image = self.sword_man_attack[int(self.attack_animation_sprite)]
    def movement(self,dt):
        if self.movement_status:
            self.vector_direction.x += (self.move_speed * dt)
            self.rect.x = round(self.vector_direction.x)
    def attack(self,dt):
        self.attacking_animations(dt)
        if self.attack_animation_sprite == 6:
            pass # code to attack another sprite
    def update(self,dt):
        self.movement(dt)
        self.walking_animation(dt)
class Archer(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
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
        self.image = self.archer_walking[self.index_walking_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))
        #ARCHMAN STATUS
        self.cost = 35
        self.health = 50
        self.demage = 4
        self.move_speed = 20
        self.animations_time = 4
        self.vector_direction = pygame.math.Vector2(self.rect.topleft)
        # MOVEMENT
        self.movement_status = True
        self.attack_status = False
    def walking_animation(self,dt):
        if self.movement_status:
            self.index_walking_sprite += (self.animations_time * dt)
            if self.index_walking_sprite >= len(self.archer_walking):
                self.index_walking_sprite = 0
            self.image = self.archer_walking[int(self.index_walking_sprite)]
    def attacking_animations(self,dt):
        self.attack_status = True
        self.movement_status = False
        if self.attack_status:
            self.index_attacking_sprite += (self.animations_time * dt)
            if self.index_attacking_sprite >= len(self.archer_attack):
                self.index_attacking_sprite = 0
            self.image = self.archer_attack[int(self.index_attacking_sprite)]
    def movement(self,dt):
        if self.movement_status:
            self.vector_direction.x += (self.move_speed * dt)
            self.rect.x = round(self.vector_direction.x)
    def attack(self,dt):
        self.attacking_animations(dt)
        if self.attack_animation_sprite == 6:
            pass # code to attack another sprite
    def update(self,dt):
        self.movement(dt)
        self.walking_animation(dt)
class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        