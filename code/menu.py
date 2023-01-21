from sys import exit
from settings import *
import pygame
from options import *
from game_mode import GameMode
from singleton import Singleton

class Menu(Singleton):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        pygame.mouse.set_visible(False)

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont("Arial", 25)
        self.menu_items = ["START", "OPTIONS", "QUIT"]
        self.current_menu_items = 0
        self.keyup_pressed = False
        self.menu_img = pygame.image.load("graphics/main_menu_images/menu_image.jpg").convert_alpha()
        self.options = Options()
    def inputs_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_menu_items = (self.current_menu_items - 1) % len(self.menu_items)
                if event.key == pygame.K_DOWN:
                    self.current_menu_items = (self.current_menu_items + 1) % len(self.menu_items)
                if event.key == pygame.K_RETURN:
                    match self.menu_items[self.current_menu_items]:
                        case "START":
                            print("STARTING GAME")
                        case "OPTIONS":
                            self.options.run()
                        case "QUIT":
                            exit()
    def draw_menu(self):
        for i,item in enumerate(self.menu_items):
            if i == self.current_menu_items:
                color = selected_color
                italic = True
                arrows = "X "
            else:
                color = (255,255,255)
                italic = False
                arrows = ""
            font = pygame.font.SysFont("Arial",40,False,italic)
            text = font.render(arrows+item,False,color)
            text_rect = text.get_rect(center=(screen_width/2,screen_heigth / 1.5 + (i * 100)))
            self.display_surface.blit(text,text_rect)
    def run(self):
        while True:
            self.fps_txt = self.font.render(str(round(main_clock.get_fps(),1)),False,(255,255,255))
            #navigation menu
            self.inputs_controls()
            #bg menu img
            self.display_surface.fill((255,0,0))
            self.display_surface.blit(self.menu_img,(-90,0))
            #drawing menu
            self.draw_menu()
            self.display_surface.blit(self.fps_txt,(0,0))
            main_clock.tick()
            pygame.display.update()
   
'''
LOGIC FOR ANIMTAION


import pygame
from math import sin, cos, atan2, degrees

# load image of emoticon with eyes
emoticon_image = pygame.image.load("emoticon.png.jpeg")
screen = pygame.display.set_mode((1200,800))
# get center and radius of the emoticon
rect = emoticon_image.get_rect()
center = rect.center
radius = rect.width // 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # calculate angle between center of emoticon and mouse
    dx = mouse_x - center[0]
    dy = mouse_y - center[1]
    angle = atan2(dy, dx)

    # calculate x and y position of eyes based on angle and radius
    eye_x = center[0] + radius * cos(angle)
    eye_y = center[1] + radius * sin(angle)

    # draw emoticon with eyes
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (255, 0, 0), (int(eye_x), int(eye_y)), 10)

    pygame.display.update()
'''