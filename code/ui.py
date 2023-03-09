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
        self.special_ui = pygame.image.load(
            "graphics/overworld/ui/special.png").convert_alpha()
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
        self.special_ui_rect = self.special_ui.get_rect(center=(1240, 160))
        # Initialize the menu items list and get the display surface
        self.menu_items = []
        self.display_surface = pygame.display.get_surface()
        # Set up font and initialize the coins and current_menu variables
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.current_menu = -1
        # status
        self.warrior_status = False
        self.sceleton_status = False
        # Load the menu items
        self.load_menu_items()
        # Timer for every unit
        self.shoutdown_sword_man = 31
        self.shoutdown_archer = 40

    def load_menu_items(self):
        self.menu_items.clear()
        if self.current_menu not in [0, 1, 2, 3]:
            for x in range(5):
                self.menu_items.append(pygame.image.load(
                    f"graphics/overworld/ui/menu_items{x}.png").convert_alpha())
            self.menu_item_rect = self.menu_items[0].get_rect(center=(970, 70))

    def show_player_building_health(self, hp, offset_x=0, offset_y=0):
        self.health_bar = pygame.transform.smoothscale(self.health_bar, (22, hp))
        self.hp_text = self.my_font.render(f"{hp}", False, (255, 0, 0))
        self.display_surface.blit(self.health_bar, (20 + offset_x, 300 + offset_y))
        self.display_surface.blit(self.hp_text, (45 + offset_x, 280 + offset_y))

    def show_enemy_building_health(self, enemy_hp, offset_x=0, offset_y=0):
        self.enemy_health_bar = pygame.transform.smoothscale(self.enemy_health_bar, (22, enemy_hp))
        self.enemy_hp_text = self.my_font.render(f"{enemy_hp}", False, (255, 0, 0))
        self.display_surface.blit(self.enemy_health_bar, (1450 + offset_x, 300 + offset_y))
        self.display_surface.blit(self.enemy_hp_text, (1420 + offset_x, 280 + offset_y))

    def mouse_inputs(self):
        self.warrior_status = False
        self.sceleton_status = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(pygame.mouse.get_pos())
                self.load_menu_items()
                for i, _ in enumerate(self.menu_items):
                    item_rect = self.menu_item_rect.move(i * 65, 0)
                    if item_rect.collidepoint(pygame.mouse.get_pos()):
                        self.current_menu = i
                        self.load_menu_items()
                        break
        self.shoutdown_sword_man += 0.1
        self.shoutdown_archer += 0.1

    def handle_mouse_click(self, mouse_pos):
        if self.back_unit_rect.collidepoint(mouse_pos):
            self.current_menu = -1
            self.load_menu_items()
        self.handle_unit_selection(mouse_pos)

    def handle_unit_selection(self, mouse_pos):
        if self.warrior_unit_rect.collidepoint(mouse_pos) \
                and self.current_menu == 0 and self.shoutdown_sword_man > 30:
            self.warrior_status = True
            self.shoutdown_sword_man -= self.shoutdown_sword_man
        elif self.sceleton_unit_rect.collidepoint(mouse_pos) \
                and self.current_menu == 0 and self.shoutdown_archer > 40:
            self.sceleton_status = True
            self.shoutdown_archer -= self.shoutdown_archer

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

    def draw_player_coins(self, player_coins):
        self.coins_text = self.my_font.render(
            f"${player_coins}",
            False,
            WHITE)
        self.display_surface.blit(self.coins_text, (44, 12))

    def draw(self, player_coins):
        self.mouse_inputs()
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
        if self.current_menu == 0:
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
        self.display_surface.blit(
            self.special_ui,
            self.special_ui_rect
        )
        self.draw_player_coins(player_coins)
