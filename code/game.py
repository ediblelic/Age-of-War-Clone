import pygame
from settings import *
from ui import UI
from unit import SwordMan,Archer
class PlayerUnitsGropu(pygame.sprite.Group):
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
        self.units = PlayerUnitsGropu()
        self.player_coins = 75
        # UNITS
        self.sword_man = SwordMan(150,600)
        self.archer = Archer(150,600)
    def check_resolution(self,full_screen):
        if full_screen:
            self.display_surface = pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
            self.fr_stage = pygame.transform.scale(self.fr_stage,(1500,720))
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
    def restart(self):
        pass
    def release_sprite(self,dt):
        if self.ui.warrior_status and self.player_coins >= self.sword_man.cost:
            self.sword_man = SwordMan(150,600)
            self.units.add(self.sword_man)
            self.player_coins -= self.sword_man.cost
        if self.ui.sceleton_status and self.player_coins >= self.archer.cost:
            self.archer = Archer(150,565)
            self.units.add(self.archer)
            self.player_coins -= self.archer.cost
        self.units.draw(self.display_surface,self.camera_x,self.camera_y)
        self.units.update(dt)
    def run(self,full_screen):
        self.running = True
        pygame.mouse.set_visible(True)
        self.check_resolution(full_screen)
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(),1)),False,(255,255,255))
            self.camera_system(dt)
            self.display_surface.fill((0,0,0))
            self.display_surface.blit(self.fr_stage,(self.camera_x,self.camera_y))
            self.ui.draw(self.player_coins)
            self.ui.show_player_building_health(220,self.camera_x,self.camera_y)
            self.ui.show_enemy_building_health(220,self.camera_x,self.camera_y)
            self.release_sprite(dt)
            self.display_surface.blit(self.fps_txt,(0,0))
            pygame.display.update()
            main_clock.tick(FPS)
