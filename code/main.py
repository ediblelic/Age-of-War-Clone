import sys, time
import pygame
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, main_clock, WHITE
from menu import Menu
from introduction import Introduction
class Main:
    """
    The main class for the Age of War game. Handles the game loop and manages game state.

    Attributes:
    - display_surface (pygame.Surface): the surface to draw game elements on
    - clock (pygame.time.Clock): the clock to control        the game's FPS
    - main_menu (Menu): the game's main menu
    - game (Game): the game itself
    - introduction (Introduction): the game's introduction
    - my_font (pygame.font.Font): the font to use for rendering text
    """

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("AGE OF WAR")
        self.main_menu = Menu().get_instance()
        self.game = Game()
        self.introduction = Introduction()
        self.my_font = pygame.font.SysFont("Arial", 20)
        self.timer = 20
    def draw_end_screen(self,fps):
        if fps == "ON":
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(), 1)), False, WHITE)
            self.display_surface.blit(self.fps_txt, (0, 0))
        self.timer -= 0.1
        if self.timer > 0:
            self.end_screen = pygame.image.load("graphics/overworld/endgame.jpg").convert()
            self.display_surface.blit(self.end_screen,(0,0))
        else:
            sys.exit()
        
    def run(self):
        """
        The game loop for the Age of War game.
        Runs continuously until the game is quit.
        While running, the function updates the game state,
        handles user input, and draws the game to the screen.
        Returns:
        - None
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_surface.fill((0, 0, 0))
            self.main_menu.run()
            self.introduction.run_story(self.main_menu.show_fps())
            self.game.run(self.main_menu.is_full_screen(),self.main_menu.difficutly(), self.main_menu.show_fps())
            self.draw_end_screen(self.main_menu.show_fps())
            pygame.display.update()
            main_clock.tick()


if __name__ == "__main__":
    main = Main()
    main.run()