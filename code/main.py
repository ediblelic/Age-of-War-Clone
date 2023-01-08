import pygame
from settings import *
from sys import exit
from menu import Menu
class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((screen_width,screen_heigth))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("AGE OF WAR")
        self.main_menu = Menu()
    def run(self):
        previous_time = time.time()
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.display_surface.fill((255,255,255))
                self.main_menu.check_window()
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":
    main = Main()
    main.run()
    