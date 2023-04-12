import math
from unit import UnitsGroup, SwordMan,Archer
from projectiles import Arrow, CatapultProjectil
from special import FireBall
from buildings import Building
from random import randrange


class Player:
    def __init__(self):
        self.player_coins = 900
        self.player_units = UnitsGroup()
        self.sword_man = SwordMan(150, 600)
        self.archer = Archer(150, 600)
        self.arrow = Arrow(0,0)
        self.catapult_projectil = CatapultProjectil(0,0)
        self.catapult_timer = 10
        self.isminigun = False
        self.player_projectiles = UnitsGroup()
        self.arrow_stack_player = UnitsGroup()
        self.fireball = FireBall(0,0)
        self.player_special = UnitsGroup()
        self.player_building = UnitsGroup()
        self.player_building.add(Building(80,550))
    
    def release_player_special(self,dt):
        duration_time = 10
        if self.ui.special_status is False and len(self.player_special) < 60 \
        and self.ui.special_shoutdown <= duration_time:
            self.sound.play_effect("fireball")
            self.fireball = FireBall(randrange(-1000,5000),randrange(-1000,0))
            self.player_special.add(self.fireball)
            self.shake_window()
        self.player_special.draw(self.display_surface,self.camera_x,self.camera_y)
        self.player_special.update(dt)
        self.clear_projectiles()
        self.kill_enemy_with_projectile()
        
    def release_player_unit(self, dt):
        if self.ui.warrior_status and self.player_coins >= self.sword_man.status.cost:
            self.sword_man = SwordMan(150, 600)
            self.player_units.add(self.sword_man)
            self.player_coins -= self.sword_man.status.cost
        if self.ui.sceleton_status and self.player_coins >= self.archer.status.cost:
            self.archer = Archer(150, 565)
            self.player_units.add(self.archer)
            self.player_coins -= self.archer.status.cost
        self.player_units.draw(self.display_surface, self.camera_x, self.camera_y)
        self.player_units.update(dt, 1)


    def is_player_in_range(self):
        try:
            fr_sprite_movement = self.enemy_units.sprites()[0].status.movement
            distance_player_enemy =  self.enemy_units.sprites()[1].rect.x - self.player_units.sprites()[0].rect.x
            if distance_player_enemy < 130  and fr_sprite_movement == False \
            and self.enemy_units.sprites()[1].name == "Archer" :
                return True
        except IndexError:
            return False
        
    def release_player_arrow(self,dt):
        try:
            if self.player_units.has(self.archer) and len(self.player_units.sprites()) > 1:
                sd_player_sprite_x = self.player_units.sprites()[1].rect.x
                sd_player_sprite_y = self.player_units.sprites()[1].rect.y
                if self.is_enemy_in_range():
                    self.player_units.sprites()[1].attack(dt,1)
                    if self.player_units.sprites()[1].release_arrow_time():
                        self.arrow_stack_player.add(Arrow(sd_player_sprite_x,sd_player_sprite_y + 40))
        except IndexError:
            pass

    def kill_player_with_special(self):
        for projectils in self.enemy_special:
            for player in self.player_units:
                if player.rect.colliderect(projectils.rect):
                    self.enemy_coins += player.status.cost
                    player.status.health -= 10000
                    projectils.kill()

    def queue_player_colision_check(self):
        player_units_queue = self.player_units.sprites()
        for sprites in range(0, len(player_units_queue)):
            fr_sprite = player_units_queue[sprites]
            try:
                each_sprite = player_units_queue[sprites + 1]
                each_sprite.enabled_movement()
                if each_sprite.rect.colliderect(fr_sprite):
                    each_sprite.stop_movement()
            except IndexError:
                pass

    def mini_gun_player(self):
        for enemy in self.enemy_units:
            if enemy.rect.x - self.ui.minigun_rect.x < 450 and self.catapult_timer >  self.catapult_projectil.delay :
                self.catapult_timer = 0
                return True
        return False
    
    def calculate_corner(self):
        try:
            enemy = self.enemy_units.sprites()[0]
            minigun = self.ui.minigun_rect
            distance = math.sqrt((enemy.rect.x - minigun.x)**2 + (enemy.rect.y - minigun.y)**2)
            target_height = enemy.rect.y + 15  - minigun.y 
            angle = math.atan2(target_height,distance)
            return float(angle * 100)
        except IndexError:
            pass