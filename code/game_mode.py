from settings import *
import pygame
class GameMode:
    def __init__(self):
        self.game_modes = ["EASY","MEDIUM","IMPOSSIBLE"]
        self.colors_difficulty = ["#33de61","#e38819","#e32a19"]
        self.index_game_mode = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
