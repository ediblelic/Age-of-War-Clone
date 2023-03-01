import time
import pygame
from pygame.sprite import spritecollide
from settings import SCREEN_HEIGHT,SCREEN_WIDTH,FPS,main_clock,WHITE
from ui import UI
from unit import SwordMan,Archer
from enemy import Enemy
class UnitsGroup(pygame.sprite.Group):
    def draw(self, surface,offset_x,offest_y):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, (spr.rect.x + offset_x,spr.rect.y + offest_y))
        self.lostsprites = []
class Game:
    def __init__(self):
        self.fr_stage = pygame.image.load("graphics/overworld/stages/fr_stage.jpg").convert()
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.display_surface = pygame.display.get_surface()
        self.fr_stage_rect = self.fr_stage.get_rect()
        self.ui = UI()
        self.camera_x = 0
        self.camera_y = 0
        self.player_coins = 75
        self.player_units = UnitsGroup()
        self.enemy_units = UnitsGroup()
        # units
        self.sword_man = SwordMan(150,600)
        self.archer = Archer(150,600)
        self.enemy = Enemy(self.sword_man.sword_man_status.cost,self.archer.archer_status.cost)
    def check_resolution(self,full_screen):
        if full_screen:
            self.display_surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
    def camera_system(self,dt):
        self.mx, self.my = pygame.mouse.get_pos()
        if self.mx in range(1200,1280):
            self.camera_x -= (300 * dt)
        if self.mx in range(0,190):
            self.camera_x += (300 * dt)
        if self.camera_x > 0:
            self.camera_x = 0
        if self.camera_x < -200:
            self.camera_x = -200
    def release_sprite(self,dt):
        if self.ui.warrior_status and self.player_coins >= self.sword_man.sword_man_status.cost:
            self.sword_man = SwordMan(150,600)
            self.player_units.add(self.sword_man)
            self.player_coins -= self.sword_man.sword_man_status.cost
        if self.ui.sceleton_status and self.player_coins >= self.archer.archer_status.cost:
            self.archer = Archer(150,565)
            self.player_units.add(self.archer)
            self.player_coins -= self.archer.archer_status.cost
        self.enemy_control_units(dt)
        self.player_units.draw(self.display_surface,self.camera_x,self.camera_y)
        self.player_units.update(dt,1)
    def queue_colision_check(self):
        collision = spritecollide(self.sword_man,self.player_units,False)
        if len(collision) > 1:
            for behind_sprite in collision:
                behind_sprite.stop_movement()
        try:
            enemy_queue_colision = spritecollide(self.enemy_sword_man,self.enemy_units,False)
            if len(enemy_queue_colision) > 1:
                for behind_sprite in enemy_queue_colision:
                    behind_sprite.stop_movement()
        except AttributeError:
            pass
    def enemy_control_units(self,dt):
        enemy_units = self.enemy.release_sprite() #info which units we realease
        if enemy_units == "Sword_man":
            self.enemy_sword_man = SwordMan(1280,600)
            self.enemy_units.add(self.enemy_sword_man)
        if enemy_units == "Archer":
            self.enemy_archer = Archer(1280,565)
            self.enemy_units.add(self.enemy_archer)
        self.enemy_units.draw(self.display_surface,self.camera_x,self.camera_y)
        self.enemy_units.update(dt,-1)
    def battle(self,dt):
        collisions = pygame.sprite.groupcollide(self.player_units, self.enemy_units, False, False)
        self.queue_colision_check()
        if collisions:
            for player_unit, enemy_unit in collisions.items():
                player_unit.stop_movement()
                player_unit.attack(dt,1)
                for enemy in enemy_unit:
                    enemy.stop_movement()
                    enemy.attack(dt,-1)
                    self.sword_man.sword_man_status.health -= self.sword_man.sword_man_status.health
                    print(self.sword_man.sword_man_status.health)
    def run(self,full_screen):
        self.running = True
        pygame.mouse.set_visible(True)
        self.check_resolution(full_screen)
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(),1)),False,WHITE)
            self.camera_system(dt)
            self.display_surface.fill((0,0,0))
            self.display_surface.blit(self.fr_stage,(self.camera_x,self.camera_y)) # bliting level
            self.ui.draw(self.player_coins)
            self.ui.show_player_building_health(220,self.camera_x,self.camera_y)
            self.ui.show_enemy_building_health(220,self.camera_x,self.camera_y)
            self.release_sprite(dt)
            self.display_surface.blit(self.fps_txt,(0,0))
            self.battle(dt)
            pygame.display.update()
            main_clock.tick(FPS)
