import time
import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, main_clock, WHITE
from ui import UI
from sound import Sound
from enemy import Enemy
from buildings import Building
from projectiles import CatapultProjectil
from camera import Camera
class Game(Enemy, Camera,Building):
    def __init__(self):
        super().__init__(15,35,500)
        Camera.__init__(self)
        self.fr_stage = pygame.image.load("graphics/overworld/stages/fr_stage.jpg").convert()
        self.fr_stage_rect = self.fr_stage.get_rect()
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.display_surface = pygame.display.get_surface()
        self.ui = UI()
        # units
        self.sound = Sound()

    
    def set_resolution(self, full_screen):
        if full_screen:
            self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    def clear_arrows(self):
        if not self.enemy_units or not self.player_units:
            self.arrow_stack_enemy.empty()
            self.arrow_stack_player.empty()
        if not self.enemy_units:
            self.player_projectiles.empty()
        if not self.player_units:
            self.enemy_projectiles.empty()

    def draw_arrows(self,dt,difficult):
        self.clear_arrows()
        for arrow in self.arrow_stack_player:
            for enemy in self.enemy_units:
                arrow.launch(dt,1)
                if arrow.rect.colliderect(enemy.rect):
                    enemy.status.health -= self.arrow.demage 
                    arrow.kill()
        for arrow in self.arrow_stack_enemy:
            for player in self.player_units:
                arrow.launch(dt,-1)
                if arrow.rect.colliderect(player.rect):
                    player.status.health -= self.arrow.demage + abs(self.set_difficulty(difficult) // 50)
                    arrow.kill()
        self.arrow_stack_player.draw(self.display_surface,self.camera_x,self.camera_y)
        self.arrow_stack_enemy.draw(self.display_surface,self.camera_x,self.camera_y)
        
    def clear_projectiles(self):
        if self.fireball.rect.y > 1800:
            self.player_special.empty()
            self.enemy_special.empty()

    def set_difficulty(self,game_difficulty):
        self.difficulty_levels = {
            "EASY": -550,
            "MEDIUM": 440,
            "HARD": 1100
        }
        return self.difficulty_levels[game_difficulty]
    
    def handle_attack(self, player, enemy, dt, diff):
        player.attack(dt,1)
        enemy.attack(dt,-1)
        if player.isattacked():
            enemy.status.health  -= player.status.demage * dt
        if enemy.isattacked():
            player.status.health -= (enemy.status.demage + self.set_difficulty(diff)) * dt
    
    def handle_death(self,diff):      
        for player in self.player_units:
            player.draw_hp(self.camera_x)
            if player.status.health <= 0:
                player.kill()
                self.enemy_coins += player.status.cost + (self.set_difficulty(diff) // 20)
                
        for enemy in self.enemy_units:
            enemy.draw_hp(self.camera_x)
            if enemy.status.health <= 0:
                enemy.kill()
                self.player_coins += enemy.status.cost
                self.sound.play_effect("add_coin")

    def move_units_after_death(self,player_queue,unit1,enemy_queue,unit2):
        if player_queue[unit1].status.health <= 0 or enemy_queue[unit2].status.health <= 0:
            player_queue[unit1].enabled_movement()
            enemy_queue[unit2].enabled_movement()
            try:
                player_queue[unit1+1].enabled_movement()
                enemy_queue[unit2+1].enabled_movement()
            except IndexError:
                pass

    def detect_collisions(self, player_unit, enemy_unit, dt, difficulty):
        enemy_queue = enemy_unit.sprites()
        player_queue = player_unit.sprites()
        for unit1 in range(len(player_queue)):
            for unit2 in range(len(enemy_queue)):
                if player_queue[unit1].rect.colliderect(enemy_queue[unit2].rect):
                    self.handle_attack(player_queue[unit1], enemy_queue[unit2], dt, difficulty)
                    self.move_units_after_death(player_queue,unit1,enemy_queue,unit2)
        self.handle_death(difficulty)

    def buy_minigun(self):
        if self.ui.isbought == "Catapult" and self.player_coins >= self.ui.price:
            self.player_coins -= self.ui.price
            self.isminigun = True

    def set_minigun(self,difficulty):
        minigun = self.ui.minigun
        minigun_rect = self.ui.minigun_rect
        enemy_minigun = self.ui.minigun_rect_enemy
        
        if self.isminigun:
            self.display_surface.blit(minigun,(minigun_rect.x + self.camera_x,minigun_rect.y))
            if self.mini_gun_player():
                self.player_projectiles.add(CatapultProjectil(minigun_rect.x,minigun_rect.y))
                self.sound.play_effect("catapult")
        if difficulty == "HARD":
            if self.mini_gun_enemy():
                self.enemy_projectiles.add(CatapultProjectil(enemy_minigun.x,enemy_minigun.y))
                self.sound.play_effect("catapult")
            self.display_surface.blit(minigun,(enemy_minigun.x + self.camera_x,enemy_minigun.y))


    def mini_gun(self,dt,diff):
        self.buy_minigun()
        self.set_minigun(diff)
        self.draw_projectiles(dt)


    def draw_projectiles(self,dt):
        for projectile in self.player_projectiles:
            for enemy in self.enemy_units:
                projectile.launch(dt,self.calculate_corner(),1)
                if projectile.rect.colliderect(enemy.rect):
                    enemy.status.health -= projectile.damage
                    projectile.kill()
        for projectile in self.enemy_projectiles:
            for player in self.player_units:
                projectile.launch(dt,self.calculate_enemy_corner(),-1)
                if projectile.rect.colliderect(player.rect):
                    player.status.health -= projectile.damage
                    projectile.kill()
        self.player_projectiles.draw(self.display_surface,self.camera_x,self.camera_y)
        self.enemy_projectiles.draw(self.display_surface,self.camera_x,self.camera_y)
        self.catapult_timer += 10 * dt
        self.catapult_timer_enemy += 10 * dt

    def battle(self,dt,difficutly):
        self.queue_player_colision_check()
        self.queue_enemy_colision_check()
        self.release_player_special(dt)
        self.release_enemy_special(dt,self.set_difficulty(difficutly))
        self.detect_collisions(self.player_units,self.enemy_units,dt,difficutly)
        self.release_player_arrow(dt)
        self.release_enemy_arrow(dt)
        self.draw_arrows(dt,difficutly)
        self.mini_gun(dt,difficutly)

    def render_fps(self,isfps):
        if isfps == "ON":
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(), 1)), False, WHITE)
            self.display_surface.blit(self.fps_txt, (0, 0))

    def draw_units(self,dt):
        self.release_player_unit(dt)
        self.release_enemy_unit(dt)

    def draw_level(self):
        ground = pygame.Color("#caab02")
        self.display_surface.fill(ground)
        self.display_surface.blit(self.fr_stage, (self.camera_x, self.camera_y))

    def gameplay(self,dt,difficulty,is_fps):
        self.draw_level()
        self.camera_system(dt)
        self.draw_units(dt)
        self.battle(dt,difficulty)
        self.building_collision(dt)
        self.ui.draw(self.player_coins,dt,self.camera_x,self.camera_y)
        self.render_fps(is_fps)

    def run(self, full_screen,game_difficulty,fps_show):
        self.running = True
        pygame.mouse.set_visible(True)
        self.set_resolution(full_screen)
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time() 
            self.gameplay(dt,game_difficulty,fps_show)
            pygame.display.update()
            main_clock.tick()
