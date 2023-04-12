import sys
import pygame
from settings import WHITE
class UI:
    def __init__(self):
        # Load the menu UI, coin UI, and special UI images
        self.menu_ui = pygame.image.load(
            "graphics/overworld/ui/menu_ui.png").convert_alpha()
        self.coin_ui = pygame.image.load(
            "graphics/overworld/ui/coin_ui.png").convert_alpha()
        # Health bar
        self.health_bar = pygame.image.load(
            "graphics/overworld/ui/health_bar.png").convert_alpha()
        self.enemy_health_bar = pygame.image.load(
            "graphics/overworld/ui/health_bar.png").convert_alpha()
        # Units
        self.warrior_unit_surface = pygame.image.load(
            "graphics/overworld/ui/unit/unit0.png").convert_alpha()
        self.warrior_unit_rect = self.warrior_unit_surface.get_rect(center=(970, 70))
        self.sceleton_unit_surface = pygame.image.load(
            "graphics/overworld/ui/unit/unit1.png").convert_alpha()
        self.sceleton_unit_rect = self.sceleton_unit_surface.get_rect(center=(1030, 70))
        self.dragon_unit_surface = pygame.image.load(
            "graphics/overworld/ui/unit/unit2.png").convert_alpha()
        self.dragon_unit_surface = pygame.transform.flip(self.dragon_unit_surface, True, False)
        self.dragon_unit_rect = self.dragon_unit_surface.get_rect(center=(1090, 70))
        self.unit_back = pygame.image.load(
            "graphics/overworld/ui/unit/unit3.png").convert_alpha()
        self.back_unit_rect = self.unit_back.get_rect(center=(1200, 70))
        # Specail attack
        self.special_ui = pygame.image.load(
            "graphics/overworld/ui/special.png").convert_alpha()
        self.special_ui_rect = self.special_ui.get_rect(center=(1240, 160))
        # Initialize the menu items list and get the display surface
        self.menu_items = []
        self.display_surface = pygame.display.get_surface()
        # Set up font and initialize the coins and current_menu variables
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.current_menu = -1
        # status
        self.player_hp = 220
        self.enemy_hp = 220
        self.warrior_status = False
        self.sceleton_status = False
        self.special_status = False
        # Load the menu items
        self.load_menu_items()
        self.load_miniguns_icons()
        # Timer for every unit
        self.shoutdown_sword_man = 31
        self.shoutdown_archer = 40
        # Timer for special
        self.special_shoutdown = 500

    def load_miniguns_icons(self):
        self.isbought = ""
        self.price = 850
        self.fr_mini_gun = pygame.image.load(
            "graphics/overworld/ui/miniguns/fr_mini_gun.png"
        ).convert_alpha()
        self.fr_mini_gun_rect = self.fr_mini_gun.get_rect(center=(970, 70))
        self.minigun = pygame.image.load(
            "graphics/overworld/ui/miniguns/minigun.png"
        ).convert_alpha()
        self.minigun_rect = self.minigun.get_rect(topleft=(100,540))
        self.minigun_rect_enemy = self.minigun.get_rect(topleft=(1430,540))

    def units_cost_text(self):
        my_font = pygame.font.SysFont("Arial", 15)
        sword_man = my_font.render("15$",False,(255,255,255))
        archer = my_font.render("35$",False,(255,255,255))
        dragon = my_font.render("90$",False,(255,255,255))
        self.display_surface.blit(sword_man,(955,60))
        self.display_surface.blit(archer,(1018,60))
        self.display_surface.blit(dragon,(1077,60))

    def miniguns_cost_text(self):
        my_font = pygame.font.SysFont("Arial", 15)
        minigun = my_font.render("850$",False,(255,255,255))
        self.display_surface.blit(minigun,(953,60))

    def load_menu_items(self):
        self.menu_items.clear()
        if self.current_menu not in [0, 1]:
            for x in range(5):
                self.menu_items.append(pygame.image.load(
                    f"graphics/overworld/ui/menu_items{x}.png").convert_alpha())
            self.menu_item_rect = self.menu_items[0].get_rect(center=(970, 70))


    def show_player_building_health(self,offset_x=0, offset_y=0):
        self.health_bar = pygame.transform.smoothscale(self.health_bar, (22, self.player_hp))
        self.hp_text = self.my_font.render(f"{int(self.player_hp)}", False, (255, 0, 0))
        self.display_surface.blit(self.health_bar, (20 + offset_x, 300 + offset_y))
        self.display_surface.blit(self.hp_text, (45 + offset_x, 280 + offset_y))

    def show_enemy_building_health(self, offset_x=0, offset_y=0):
        self.enemy_health_bar = pygame.transform.smoothscale(self.enemy_health_bar, (22, self.enemy_hp))
        self.enemy_hp_text = self.my_font.render(f"{int(self.enemy_hp)}", False, (255, 0, 0))
        self.display_surface.blit(self.enemy_health_bar, (1450 + offset_x, 300 + offset_y))
        self.display_surface.blit(self.enemy_hp_text, (1420 + offset_x, 280 + offset_y))
    
    def handle_special_attack(self):
        if self.special_ui_rect.collidepoint(pygame.mouse.get_pos()) \
        and self.special_shoutdown >= 100 and self.special_status:
            self.special_status = False
            self.special_shoutdown = 0


    def mouse_inputs(self,dt):
        self.warrior_status = False
        self.sceleton_status = False
        self.isbought = "None"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(pygame.mouse.get_pos())
                self.load_menu_items()
                self.handle_special_attack()
                for i, _ in enumerate(self.menu_items):
                    item_rect = self.menu_item_rect.move(i * 65, 0)
                    if item_rect.collidepoint(pygame.mouse.get_pos()):
                        self.current_menu = i
                        self.load_menu_items()
                        break
        self.special_shoutdown += 10 * dt
        self.shoutdown_sword_man += 10 * dt
        self.shoutdown_archer += 10 * dt

    def handle_mouse_click(self, mouse_pos):
        if self.back_unit_rect.collidepoint(mouse_pos):
            self.current_menu = -1
            self.load_menu_items()
        self.handle_unit_selection(mouse_pos)
        self.handle_miniguns_selection()

    def handle_unit_selection(self, mouse_pos):
        if self.warrior_unit_rect.collidepoint(mouse_pos) \
                and self.current_menu == 0 and self.shoutdown_sword_man > 30:
            self.warrior_status = True
            self.shoutdown_sword_man -= self.shoutdown_sword_man
        elif self.sceleton_unit_rect.collidepoint(mouse_pos) \
                and self.current_menu == 0 and self.shoutdown_archer > 40:
            self.sceleton_status = True
            self.shoutdown_archer -= self.shoutdown_archer

    def handle_miniguns_selection(self):
        if self.fr_mini_gun_rect.collidepoint(pygame.mouse.get_pos()) \
        and self.current_menu == 1:
            self.isbought = "Catapult"

    def disabled_specail(self):
        disabled_surface = pygame.Surface((67,40))
        disabled_surface.fill((0,0,0))
        disabled_surface.set_alpha(132)
        if self.special_shoutdown >= 500:
            self.special_status = True
        if self.special_status is False:
            self.display_surface.blit(disabled_surface,(1205,142))

    def shoutdown_unit(self, player_coins):
        self.disabled_surface = [
            pygame.Surface((40, 40)),
            pygame.Surface((40, 40)),
            pygame.Surface((40, 40))
        ]
        if player_coins < 15:
            for i, surface in enumerate(self.disabled_surface):
                surface.set_alpha(150)
                surface.fill((0, 0, 0))
                self.display_surface.blit(surface, (950 + (i * 60), 50))
        if self.shoutdown_sword_man < 29 and player_coins > 15:
            self.disabled_surface = pygame.Surface((40, 40))
            self.disabled_surface.set_alpha(122)
            self.disabled_surface.fill((0, 0, 0))
            self.display_surface.blit(self.disabled_surface, (950, 50))
        if self.shoutdown_archer < 39 and player_coins > 15:
            self.disabled_surface = pygame.Surface((40, 40))
            self.disabled_surface.set_alpha(122)
            self.disabled_surface.fill((0, 0, 0))
            self.display_surface.blit(self.disabled_surface, (1010, 50))
        dragon_disabled = pygame.Surface((40,40))
        dragon_disabled.set_alpha(122)
        dragon_disabled.fill((0,0,0))
        self.display_surface.blit(dragon_disabled,(1073,50))

    def draw_player_coins(self, player_coins):
        self.coins_text = self.my_font.render(
            f"${player_coins}",
            False,
            WHITE)
        self.display_surface.blit(self.coins_text, (44, 12))

    def draw_units_ui(self,player_coins):
        self.display_surface.blit(
                self.warrior_unit_surface,
                self.warrior_unit_rect
            )
        self.display_surface.blit(
            self.sceleton_unit_surface, self.
            sceleton_unit_rect
        )
        self.display_surface.blit(
            self.dragon_unit_surface,
            self.dragon_unit_rect
        )
        self.display_surface.blit(
            self.unit_back,
            self.back_unit_rect
        )
        self.shoutdown_unit(player_coins)
        self.units_cost_text()
    
    
    def draw_miniguns(self):
        self.display_surface.blit(self.fr_mini_gun,self.fr_mini_gun_rect)
        self.display_surface.blit(
            self.unit_back,
            self.back_unit_rect
        )
        self.miniguns_cost_text()

    def state_control(self,player_coins):
        if self.current_menu == 0:
            self.draw_units_ui(player_coins)
        if self.current_menu == 1:
            self.draw_miniguns()

    def draw(self, player_coins,dt,camera_x,camera_y):
        # Draw the menu UI and coin UI on the display surface
        self.display_surface.blit(self.menu_ui, (900, 0))
        self.display_surface.blit(self.coin_ui, (0, 0))
        # Draw the menu items on the display surface
        for i, item in enumerate(self.menu_items):
            self.display_surface.blit(
                item,
                (self.menu_item_rect.x + (i * 65), self.menu_item_rect.y)
            )
        # Draw the unit items on the display surface
        self.state_control(player_coins)
        self.display_surface.blit(
            self.special_ui,
            self.special_ui_rect
        )
        self.disabled_specail()
        self.draw_player_coins(player_coins)
        self.mouse_inputs(dt)
        self.show_player_building_health(camera_x, camera_y)
        self.show_enemy_building_health(camera_x, camera_y)
