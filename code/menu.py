import sys
import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SELECTED_COLOR, WHITE, main_clock
from options import Options
from singleton import Singleton
class Menu(Singleton):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.display_surface = pygame.display.get_surface()
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.menu_items = ["START", "OPTIONS", "QUIT"]
        self.current_menu_items = 0
        self.keyup_pressed = False
        self.menu_img = pygame.image.load("graphics/main_menu_images/menu_image.jpg").convert()
        pygame.mouse.set_visible(False)
        self.options = Options()
        self.running = True
        self.menu_img.set_alpha(255)
        self.transtion_step = 5
        self.transtion = True

    def menu_transition(self):
        if self.transtion:
            self.menu_img.set_alpha(self.menu_img.get_alpha() + self.transtion_step)
            if self.menu_img.get_alpha() > 255:
                self.transtion = False

    def inputs_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_menu_items = (self.current_menu_items - 1) % len(self.menu_items)
                if event.key == pygame.K_DOWN:
                    self.current_menu_items = (self.current_menu_items + 1) % len(self.menu_items)
                if event.key == pygame.K_RETURN:
                    match self.menu_items[self.current_menu_items]:
                        case "START":
                            self.difficutly()
                            self.running = False
                        case "OPTIONS":
                            self.menu_img.set_alpha(0)
                            self.options.run()
                        case "QUIT":
                            sys.exit()

    def difficutly(self):
        return self.options.game_modes[self.options.index_game_mode]
    
    def show_fps(self):
        return self.options.rain_status[self.options.rain_system_index]

    def is_full_screen(self):
        return self.options.full_screen

    def draw_menu(self):
        for i, item in enumerate(self.menu_items):
            if i == self.current_menu_items:
                color = SELECTED_COLOR
                italic = True
                arrows = "X "
            else:
                color = (255, 255, 255)
                italic = False
                arrows = ""
            font = pygame.font.SysFont("Arial", 40, False, italic)
            text = font.render(arrows + item, False, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5 + (i * 100)))
            self.display_surface.blit(text, text_rect)

    def render_fps(self,isfps):
        if isfps == "ON":
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(), 1)), False, WHITE)
            self.display_surface.blit(self.fps_txt, (0, 0))

    def run(self):
        while self.running:
            self.menu_transition()
            self.inputs_controls()
            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.menu_img, (-90, 0))
            self.draw_menu()
            self.render_fps(self.show_fps())
            main_clock.tick()
            pygame.display.update()
