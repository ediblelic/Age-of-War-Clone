from settings import *
import pygame
from sys import exit
from  menu import  Menu
from introduction import Introduction
class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((screen_width,screen_heigth))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("AGE OF WAR")
        self.main_menu = Menu().get_instance()
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.introduction = Introduction()
    def run(self):
        previous_time = time.time()
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(),1)),False,(255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display_surface.fill((0,0,0))
            self.main_menu.run()
            self.introduction.run_story()
            self.display_surface.blit(self.fps_txt,(0,0))
            pygame.display.update()
            main_clock.tick()
if __name__ == "__main__":
    main = Main()
    main.run()
    