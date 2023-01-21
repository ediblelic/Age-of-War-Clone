from settings import *
import pygame
from sys import exit
from  menu import  Menu

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((screen_width,screen_heigth))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("AGE OF WAR")
        self.main_menu = Menu().get_instance()
    def run(self):
        previous_time = time.time()
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display_surface.fill((0,0,0))
            self.main_menu.run()
            pygame.display.update()
            main_clock.tick(FPS)
if __name__ == "__main__":
    main = Main()
    main.run()
    