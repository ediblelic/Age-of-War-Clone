from settings import *
import pygame
from sound import Sound
class Options:
    def __init__(self):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.display_surface = pygame.display.get_surface()
        self.rain_status = ["OFF","ON"]
        self.sound_system = ['OFF','ON']
        self.sound_system_index = 0
        self.rain_system_index = 0
        self.options_items = ["SOUND","RAIN","FULLSCREEN"]
        self.curr_options_items = 0
        self.options_img = pygame.image.load("graphics/main_menu_images/options_img.jpg").convert_alpha()
        self.sound = Sound()
        #  OPTIONS TEXT  #
        self.back_text = self.my_font.render("Back", False, "yellow")
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_DOWN:
                    self.curr_options_items = (self.curr_options_items + 1) % len(self.options_items)
                if event.key == pygame.K_UP:
                    self.curr_options_items = (self.curr_options_items - 1) % len(self.options_items)
                if event.key == pygame.K_RETURN:
                    match self.options_items[self.curr_options_items]:
                        case "SOUND":
                            print("STARTING GAME")
                        case "RAIN":
                            pass
                        case "FULLSCREEN":
                            self.display = pygame.display.set_mode((screen_width,screen_heigth),pygame.FULLSCREEN)
    def draw_options(self):
        for i,opt_item in enumerate(self.options_items):
            if i == self.curr_options_items:
                color = selected_color
                arrows = "X "
                italic = True
            else:
                color = (255,255,255)
                arrows = ""
                italic = False
            font = pygame.font.SysFont("Arial",40,False,italic)
            options_text = font.render(arrows + opt_item,False,color)
            options_text_rect = options_text.get_rect(center=(screen_width/2,screen_heigth / 1.5 + (i * 100)))
            self.display_surface.blit(options_text,options_text_rect)
    def run(self):
        self.running = True
        while self.running:
            self.inputs()

            self.display_surface.fill((255,0,0))
            self.display_surface.blit(self.options_img,(-90,0))
            self.draw_options()
            main_clock.tick(FPS)
            pygame.display.update()
