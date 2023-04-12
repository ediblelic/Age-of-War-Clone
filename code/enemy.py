import random, math
from buildings import Building
from unit import UnitsGroup, SwordMan, Archer
from player import Player
from special import FireBall
from projectiles import Arrow

class Enemy(Player):
    def __init__(self, sword_man_cost, archer_cost,enemy_coins):
        super().__init__()
        self.sword_man_cost = sword_man_cost
        self.archer_cost = archer_cost
        self.shoutdown = 0
        self.specail_delay = 300
        self.enemy_coins = enemy_coins
        self.enemy_units = UnitsGroup()
        self.enemy_projectiles = UnitsGroup()
        self.arrow_stack_enemy = UnitsGroup()
        self.enemy_special = UnitsGroup()
        self.enemy_building = UnitsGroup()
        self.enemy_building.add(Building(1350,550))
        self.catapult_timer_enemy = 10
        
    def choose_unit(self,dt):
        self.shoutdown += 10 * dt
        self.ai = random.randint(0,100)
        if self.enemy_coins >= self.sword_man_cost and self.shoutdown >= 50 and self.ai == 22:
            self.shoutdown = 0
            self.enemy_coins -= self.sword_man_cost
            return "Sword_man"
        if self.enemy_coins >= self.archer_cost and self.shoutdown >= 60 and self.ai == 33:
            self.shoutdown = 0
            self.enemy_coins -= self.archer_cost
            return "Archer"
        return None

    

    def activate_special(self,dt,game_difficulty):
        self.specail_delay += 10 * dt
        timer_to_activate_fireballs = 1000 - (game_difficulty / 2)
        if self.specail_delay > timer_to_activate_fireballs :
            self.specail_delay = 0
            return "Special"
        return None
    

    def release_enemy_special(self,dt,game_difficulty):
        duration_time = 10
        if self.activate_special(dt,game_difficulty) == "Special" \
        or self.specail_delay < duration_time:
            self.fireball = FireBall(random.randrange(-1000,5000),random.randrange(-1000,0))
            self.enemy_special.add(self.fireball)
            self.sound.play_effect("fireball")
            self.shake_window()
        self.enemy_special.draw(self.display_surface,self.camera_x,self.camera_y)
        self.enemy_special.update(dt)
        self.kill_player_with_special()

    def kill_enemy_with_projectile(self):
        for projectils in self.player_special:
            for enemy in self.enemy_units:
                if enemy.rect.colliderect(projectils.rect):
                    self.player_coins += enemy.status.cost
                    self.sound.play_effect("add_coin")
                    enemy.status.health -= 10000
                    projectils.kill()

    def release_enemy_unit(self, dt):
        picked_enemy_unit = self.choose_unit(dt) 
        if picked_enemy_unit == "Sword_man":
            self.enemy_sword_man = SwordMan(1280, 600)
            self.enemy_units.add(self.enemy_sword_man)
        if picked_enemy_unit == "Archer":
            self.enemy_archer = Archer(1280, 565)
            self.enemy_units.add(self.enemy_archer)
        self.enemy_units.draw(self.display_surface, self.camera_x, self.camera_y)
        self.enemy_units.update(dt, -1)

    def is_enemy_in_range(self):
        try:
            fr_sprite_movement = self.player_units.sprites()[0].status.movement
            distance_player_enemy =  self.enemy_units.sprites()[0].rect.x - self.player_units.sprites()[1].rect.x
            if distance_player_enemy < 135 and fr_sprite_movement == False \
            and self.player_units.sprites()[1].name == "Archer" :
                return True
        except IndexError:
            return False
        
    def release_enemy_arrow(self,dt):
        try:
            if self.enemy_units.has(self.enemy_archer) and len(self.enemy_units.sprites()) > 1:
                    sd_enemy_sprite_x = self.enemy_units.sprites()[1].rect.x
                    sd_enemy_sprite_y = self.enemy_units.sprites()[1].rect.y
                    if self.is_player_in_range():
                        self.enemy_units.sprites()[1].attack(dt,-1)
                        if self.enemy_units.sprites()[1].release_arrow_time():
                            self.arrow_stack_enemy.add(Arrow(sd_enemy_sprite_x,sd_enemy_sprite_y + 40))
        except AttributeError:
            pass

    def queue_enemy_colision_check(self):
        enemy_units_queue = self.enemy_units.sprites()
        for sprites in range(0, len(enemy_units_queue)):
            fr_sprite = enemy_units_queue[sprites]
            try:
                each_sprite = enemy_units_queue[sprites + 1]
                each_sprite.enabled_movement()
                if each_sprite.rect.colliderect(fr_sprite):
                    each_sprite.stop_movement()
                else:
                    each_sprite.enabled_movement()
            except IndexError:
                pass

    def mini_gun_enemy(self):
        for enemy in self.player_units:
            if enemy.rect.x - self.ui.minigun_rect_enemy.x > -450 and self.catapult_timer_enemy >  self.catapult_projectil.delay :
                self.catapult_timer_enemy = 0
                return True
        return False
    
    def calculate_enemy_corner(self):
        try:
            enemy = self.player_units.sprites()[0]
            minigun_enemy = self.ui.minigun_rect_enemy
            distance =  math.sqrt((minigun_enemy.x - enemy.rect.x)**2 + (minigun_enemy.y - enemy.rect.y)**2)
            target_height = enemy.rect.y + 30 - minigun_enemy.y
            angle = math.atan2(target_height,distance)
            return float(angle * 100)
        except IndexError:
            pass