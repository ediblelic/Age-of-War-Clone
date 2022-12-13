import pygame 
from sys import exit
from settings import *
from pygame.mouse import get_pos as mouse_position
class Options:
    def __init__(self):
        self.acitve = False
    def turn_off_sound(self):
        pass
class Game:
    def __init__(self):
        pass
    def game_mode(self,mode):
        pass
    def start(self):
        pass
class Menu:
    def __init__(self):
        self.options = Options()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.main_title_game = self.my_font.render("A G E - O F - W A R",False,"yellow")
        self.display_surface = pygame.display.get_surface()
        self.inputs()
        self.set_cursor()
        self.menu_text()
        self.blit_text()
    def set_cursor(self):
        self.cursor_surface = pygame.image.load("graphics/overworld/cursor.png")
        self.cursor_surface = pygame.transform.scale(self.cursor_surface,(50,50))
        self.mouse_pos = mouse_position()
        self.cursor_surface_rect = self.cursor_surface.get_rect()

    def menu_text(self):
        self.start_text = self.my_font.render("X START X",False,"yellow")
        self.options_text = self.my_font.render("X OPTIONS X", False, "yellow")
        self.exit_text = self.my_font.render("X EXIT X", False, "yellow")
    def inputs(self):
        self.mouse_pressed = pygame.mouse.get_pressed()
        if self.mouse_pressed
    
    def blit_text(self):
        self.display_surface.fill("#2596be")
        self.display_surface.blit(self.main_title_game,(screen_width // 3,screen_heigth//8))
        self.display_surface.blit(self.start_text,(screen_width // 2,screen_heigth//2 - 50))
        self.display_surface.blit(self.options_text,(screen_width // 2,screen_heigth - 300))
        self.display_surface.blit(self.exit_text,(screen_width // 2,screen_heigth- 200))
        self.display_surface.blit(self.cursor_surface,(self.mouse_pos))
        if self.options.acitve:
            exit()    
    def exit_game(self):
        exit()