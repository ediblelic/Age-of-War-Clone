import pygame 
from sys import exit
from settings import *
from pygame.mouse import get_pos as mouse_position
class Options:
    def __init__(self):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.display_surface = pygame.display.get_surface()
        self.rain_status = ["OFF","ON"]
        self.sound_system = ['OFF','ON']
        self.sound_system_index = 0
        self.rain_system_index = 0
        #  OPTIONS TEXT  #
        self.back_text = self.my_font.render("Back", False, "yellow")
    def inputs_options(self) -> str:
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = mouse_position()
        self.mouse_x = self.mouse_pos[0]
        self.mouse_y = self.mouse_pos[1]
        print(self.mouse_pos)
        #   RETURN TO MENU   #
        if self.is_menu():
            return "MENU"
        return "OPTIONS"
    def is_menu(self) -> bool:
        if self.mouse_x in range(626,721) and self.mouse_y in range(532,560) and self.mouse_pressed[0]:
            return True
        return False
    def is_left_arrow(self) -> bool:
        if self.mouse_x in range(785,813) and self.mouse_y in range(311,352) and self.mouse_pressed[0]:
            return True
        return False
    def is_right_arrow(self) -> bool:
        if self.mouse_x in range(917,980) and self.mouse_y in range(315,342) and self.mouse_pressed[0]:
            return True
        return False
    def turn_off_sound(self) -> str:
        if self.is_left_arrow():
            self.sound_system_index -= 1
            if self.sound_system_index == -2:
                self.sound_system_index = 1
        if self.is_right_arrow():
            self.sound_system_index +=1
            if self.sound_system_index > len(self.sound_system) - 1:
                self.sound_system_index = 0
        return self.sound_system[self.sound_system_index]
    def is_left_arrow_rain(self) -> bool:
        if self.mouse_x in range(750,769) and self.mouse_y in range(430,462) and self.mouse_pressed[0]:
            return True
        return False
    def is_right_arrow_rain(self) -> bool:
        if self.mouse_x in range(878,922) and self.mouse_y in range(430,462) and self.mouse_pressed[0]:
            return True
        return False
    def turn_off_rain(self) -> str:
        if self.is_left_arrow_rain():
            self.rain_system_index -= 1
            if self.rain_system_index == -2:
                self.rain_system_index = 1
        if self.is_right_arrow_rain():
            self.rain_system_index +=1
            if self.rain_system_index > len(self.rain_status) - 1:
                self.rain_system_index = 0
        return self.rain_status[self.rain_system_index]
    def blit_options_text(self):
        #     BACKGROUND FILL    #
        self.display_surface.fill("#2596be")
        #  DISPLAY RAIN OFF/ON   #
        self.rain_effect = self.my_font.render(f"Rain: < {self.turn_off_rain()} >", False, "yellow")
        self.display_surface.blit(self.rain_effect,(screen_width // 2,screen_heigth - 300))
        #     BACK TO MENU       #
        self.display_surface.blit(self.back_text,(screen_width // 2,screen_heigth- 200))
        #  DISPLAY SOUND OFF/ON  #
        self.sound = self.my_font.render(f"Sound: < {self.turn_off_sound()} >",False,"yellow")
        self.display_surface.blit(self.sound,(screen_width // 2,screen_heigth//2 - 50))
class GameMode:
    def __init__(self):
        self.game_modes = ["EASY","MEDIUM","IMPOSSIBLE"]
        self.colors_difficulty = ["#33de61","#e38819","#e32a19"]
        self.index_game_mode = 0
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.display_surface = pygame.display.get_surface()
        self.back_text = self.my_font.render("Back", False, "yellow")
        self.game_mode_title = self.my_font.render("Game Mode:", False, "yellow")
        self.game_mode_left_arrow = self.my_font.render(f"<", False, "yellow")
        self.game_mode_right_arrow = self.my_font.render(f">", False, "yellow")

    def inputs(self) -> str:
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = mouse_position()
        self.mouse_x = self.mouse_pos[0]
        self.mouse_y = self.mouse_pos[1]
        #   BACK BUTTON   #
        if self.mouse_x > 626 and self.mouse_x < 721 and self.mouse_y > 532 and self.mouse_y < 560 and self.mouse_pressed[0]:
            return "MENU"
        return "GAME MODE"
    def set_game_mode(self) -> str:
        # if maous_x range (899) and maouse_y range(400,900)
        if self.mouse_x > 899 and self.mouse_x < 918 and self.mouse_y > 370 and self.mouse_y < 400 and self.mouse_pressed[0] and self.index_game_mode > 0:
            self.index_game_mode -= 1
        if self.mouse_x > 1078 and self.mouse_x < 1100 and self.mouse_y > 370 and self.mouse_y < 400 and self.mouse_pressed[0]:
            self.index_game_mode += 1
            if self.index_game_mode  > len(self.game_modes) - 1:
                self.index_game_mode = 0
                return self.game_modes[self.index_game_mode]
            return self.game_modes[self.index_game_mode]
        return self.game_modes[self.index_game_mode]
    def start(self):
        pass
    def blit_game_mode_text(self):
        self.display_surface.fill(self.colors_difficulty[self.index_game_mode])
        #    CHANGING GAME MODE       #
        self.display_surface.blit(self.game_mode_title,(screen_width // 2,screen_heigth // 2))
        self.display_surface.blit(self.game_mode_left_arrow,(921, 360))
        self.display_surface.blit(self.game_mode_right_arrow,(1100, 360))
        self.difficulty_font = pygame.font.SysFont('Comic Sans MS', 100 // len(self.game_modes[self.index_game_mode]) + 10)
        self.game_mode_text = self.difficulty_font.render(self.set_game_mode(),False,"yellow")
        self.display_surface.blit(self.game_mode_text,(960,367 + (len(self.game_modes[self.index_game_mode])) * 2))
        self.display_surface.blit(self.back_text,(screen_width // 2,screen_heigth- 200))
class Menu:
    def __init__(self):
        self.my_font = pygame.font.SysFont('Comic Sans MS', 50)
        self.main_title_game = self.my_font.render("A G E - O F - W A R",False,"yellow")
        self.display_surface = pygame.display.get_surface()
        self.current_window = "MENU"
        self.options = Options()
        self.game_mode_win = GameMode()
        pygame.mouse.set_visible(False)
    def set_cursor(self):
        self.cursor_surface = pygame.image.load("graphics/overworld/cursor.png")
        self.cursor_surface = pygame.transform.scale(self.cursor_surface,(50,50))
        self.mouse_pos = mouse_position()
        self.mouse_x = self.mouse_pos[0]
        self.mouse_y = self.mouse_pos[1]
        self.cursor_surface_rect = self.cursor_surface.get_rect()
    def menu_text(self):
        self.start_text = self.my_font.render("X START X",False,"yellow")
        self.options_text = self.my_font.render("X OPTIONS X", False, "yellow")
        self.exit_text = self.my_font.render("X EXIT X", False, "yellow")
    def is_game_mode(self) -> bool:
        if self.mouse_x in range(677,831) and self.mouse_y in range(325,351) and self.mouse_pressed[0]:
            return True
        return False
    def is_options(self):
        if self.mouse_x in range(677,905) and self.mouse_y in range(425,460) and self.mouse_pressed[0]:
            return True
        return False
    def inputs(self):
        self.mouse_pressed = pygame.mouse.get_pressed()
        #   GAME MODE  #
        if self.is_game_mode():
            self.current_window = "GAME MODE"
        #   OPTIONS    #
        if self.is_options():
            self.current_window = "OPTIONS"
        #   EXIT GAME  #
        if self.mouse_x > 677 and self.mouse_x < 830 and self.mouse_y > 520 and self.mouse_y < 566 and self.mouse_pressed[0]:
            exit()
    def blit_text_menu(self):
        self.display_surface.fill("#2596be")
        self.display_surface.blit(self.start_text,(screen_width // 2,screen_heigth//2 - 50))
        self.display_surface.blit(self.options_text,(screen_width // 2,screen_heigth - 300))
        self.display_surface.blit(self.exit_text,(screen_width // 2,screen_heigth- 200))
    def run_menu(self):
        self.menu_text()
        self.inputs()
        self.blit_text_menu()
    def run_options(self):
        self.options.inputs_options()
        self.options.blit_options_text()
    def run_game_mode(self):
        self.game_mode_win.inputs()
        self.game_mode_win.blit_game_mode_text()
    def check_window(self):
        self.set_cursor()
        match self.current_window:
            case "MENU":
                self.run_menu()
            case "OPTIONS":
                self.run_options()
                self.current_window = self.options.inputs_options()
            case "GAME MODE":
                self.run_game_mode()
                self.current_window = self.game_mode_win.inputs()
            case "START GAME":
                return self.current_window
        self.display_surface.blit(self.main_title_game,(screen_width // 3,screen_heigth//8))
        self.display_surface.blit(self.cursor_surface,(self.mouse_pos))
