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
    animation_time: int
    movement: bool
    attack: bool

class UnitsGroup(pygame.sprite.Group):
    def draw(self, surface, offset_x, offset_y):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, (spr.rect.x + offset_x, spr.rect.y + offset_y))
        self.lostsprites = []


class SwordMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # LOADING SPRITES
        self.name = "SwordMan"
        self.load_sprites()
        self.image = self.sword_man_walking[self.current_sword_man_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        # SWORDMAN STATUS
        self.status = Status(15, 2000, 1100, 100, 8, True, False)
        self.vector_direction = pygame.math.Vector2(self.rect.topleft)

    def load_sprites(self):
        self.sword_man_walking = []
        self.sword_man_attack = []
        self.display_surface = pygame.display.get_surface()
        # LOADING SPRITES
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

    def walking_animation(self, dt):
        if self.status.movement:
            self.current_sword_man_sprite += (self.status.animation_time * dt)
            if self.current_sword_man_sprite >= len(self.sword_man_walking):
                self.current_sword_man_sprite = 0

    def attacking_animations(self, dt, enemy):
        self.status.attack = True
        self.status.movement = False
        if self.status.attack:
            self.attack_animation_sprite += (self.status.animation_time * dt)
            if self.attack_animation_sprite >= len(self.sword_man_attack):
                self.attack_animation_sprite = 0
            if enemy == -1:
                self.image = pygame.transform.flip(self.sword_man_attack[int(self.attack_animation_sprite)], True,
                                                   False)
            else:
                self.image = self.sword_man_attack[int(self.attack_animation_sprite)]

    def movement(self, dt, enemy):
        prev_x = self.vector_direction.x
        if self.status.movement:
            self.vector_direction.x += (self.status.move_speed * dt) * enemy
            self.rect.x = round(self.vector_direction.x)
        if self.vector_direction.x <= prev_x and enemy == -1:
            self.image = pygame.transform.flip(self.sword_man_walking[int(self.current_sword_man_sprite)], True, False)
        else:
            self.image = self.sword_man_walking[int(self.current_sword_man_sprite)]


    def stop_movement(self):
        self.status.movement = False


    def enabled_movement(self):
        self.status.movement = True


    def draw_hp(self,camera):
        hp_width = self.status.health / 40
        hp_height = 4
        offset_x = self.rect.x + camera + 8
        offset_y = self.rect.y + 80
        try:
            player_hp = pygame.Surface((hp_width, hp_height))
            player_hp.fill((255,0,0))
            self.display_surface.blit(player_hp,(offset_x,offset_y))
        except pygame.error:
            pass

    def demage(self):
        return self.status.demage
    
    def isattacked(self):
        if self.attack_animation_sprite > 8:
            return True
        return False
    

    def attack(self, dt, enemy):
        self.attacking_animations(dt, enemy)

    def update(self, dt, enemy):
        self.movement(dt, enemy)
        self.walking_animation(dt)


class Archer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # Loading sprites
        self.name = "Archer"
        self.load_sprites()
        self.image = self.archer_walking[self.index_walking_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        # ARCHMAN STATUS
        self.status = Status(35, 3000, 740, 80, 12, True, False)
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

    def walking_animation(self, dt):
        if self.status.movement:
            self.index_walking_sprite += (self.status.animation_time * dt)
            if self.index_walking_sprite >= len(self.archer_walking):
                self.index_walking_sprite = 0

    def attacking_animations(self, dt, isenemy):
        self.status.attack = True
        self.status.movement = False
        if self.status.attack:
            self.index_attacking_sprite += (self.status.animation_time * dt)
            if self.index_attacking_sprite >= len(self.archer_attack):
                self.index_attacking_sprite = 0
            if isenemy ==  1:
                self.image = pygame.transform.flip(
                    self.archer_attack[int(self.index_attacking_sprite)],
                    True,
                    False
                    )
            else:
                self.image = self.archer_attack[int(self.index_attacking_sprite)]
    def release_arrow_time(self):
        if self.index_attacking_sprite > 8.0 and self.index_attacking_sprite < 9.0:
            return True
        return False
    def movement(self, dt, enemy):
        prev_x = self.vector_direction.x
        if self.status.movement:
            self.vector_direction.x += (self.status.move_speed * dt) * enemy
            self.rect.x = round(self.vector_direction.x)
        if self.vector_direction.x < prev_x and enemy == -1:
            self.image = pygame.transform.flip(self.archer_walking[int(self.index_walking_sprite)], True, False)
        else:
            self.image = self.archer_walking[int(self.index_walking_sprite)]

    def stop_movement(self):
        self.status.movement = False


    def enabled_movement(self):
        self.status.movement = True


    def draw_hp(self,camera):
        hp_width = self.status.health / 60
        hp_height = 4
        offset_x = self.rect.x + camera + 8
        offset_y = self.rect.y + 115
        try:
            player_hp = pygame.Surface((hp_width, hp_height))
            player_hp.fill((255,0,0))
            self.display_surface.blit(player_hp,(offset_x,offset_y))
        except pygame.error:
            pass
        
    def demage(self):
        return self.status.demage
    

    def isattacked(self):
        if self.index_attacking_sprite > 8:
            return True
        return False
    

    def attack(self, dt,isenemy):
        self.attacking_animations(dt, isenemy)

    def update(self, dt, enemy):
        self.movement(dt, enemy)
        self.walking_animation(dt)


class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass
