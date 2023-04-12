import sys
import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SELECTED_COLOR, WHITE, main_clock
from sound import Sound


class Options:
    def __init__(self):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', 20)
        self.display_surface = pygame.display.get_surface()
        self.rain_status = ["OFF", "ON"]
        self.sound_system = ['OFF', 'ON']
        self.options_items = ["DIFFICULTY", "SOUND", "FPS", "RESOLUTION"]
        self.resolution = [f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}", "Fullscreen"]
        self.game_modes = ["EASY", "MEDIUM", "HARD"]
        self.colors_difficulty = ["#33de61", "#e38819", "#e32a19"]
        self.index_game_mode = 0
        self.resolution_index = 0
        self.sound_system_index = 0
        self.rain_system_index = 0
        self.curr_options_items = 0
        self.options_img = pygame.image.load("graphics/main_menu_images/options_img.jpg").convert()
        self.sound = Sound()
        self.options_img.set_alpha(0)
        self.transtion_step = 5
        self.transtion = True
        self.full_screen = False

    def options_transtion(self):
        if self.transtion:
            self.options_img.set_alpha(self.options_img.get_alpha() + self.transtion_step)
            if self.options_img.get_alpha() > 255:
                self.transtion = False

    def handle_quit_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit()

    def handle_keydown_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
            self.options_img.set_alpha(0)
        if event.key == pygame.K_DOWN:
            self.curr_options_items = (self.curr_options_items + 1) % len(self.options_items)
        if event.key == pygame.K_UP:
            self.curr_options_items = (self.curr_options_items - 1) % len(self.options_items)
        if event.key == pygame.K_RIGHT:
            self.handle_right_key()
        if event.key == pygame.K_LEFT:
            self.handle_left_key()
        if event.key == pygame.K_RETURN:
            self.handle_return_key()

    def handle_right_key(self):
        option = self.options_items[self.curr_options_items]
        if option == "SOUND":
            self.sound.toggle_bg_music_on()
            self.sound_system_index = (self.sound_system_index + 1) % len(self.sound_system)
        elif option == "FPS":
            self.rain_system_index = (self.rain_system_index + 1) % len(self.rain_status)
        elif option == "RESOLUTION":
            self.resolution_index = (self.resolution_index + 1) % len(self.resolution)
        elif option == "DIFFICULTY":
            self.index_game_mode = (self.index_game_mode + 1) % len(self.game_modes)

    def handle_left_key(self):
        option = self.options_items[self.curr_options_items]
        if option == "SOUND":
            self.sound.toggle_bg_music_on()
            self.sound_system_index = (self.sound_system_index - 1) % len(self.sound_system)
        elif option == "FPS":
            self.rain_system_index = (self.rain_system_index - 1) % len(self.rain_status)
        elif option == "RESOLUTION":
            self.resolution_index = (self.resolution_index - 1) % len(self.resolution)
        elif option == "DIFFICULTY":
            self.index_game_mode = (self.index_game_mode - 1) % len(self.game_modes)

    def handle_return_key(self):
        option = self.options_items[self.curr_options_items]
        if option == "RESOLUTION" and self.resolution_index == 1:
            self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            self.full_screen = not self.full_screen
        elif option == "RESOLUTION" and self.resolution_index == 0:
            self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def inputs(self):
        for event in pygame.event.get():
            self.handle_quit_event(event)
            if event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)


    def resize_text(self, curr_item_options):
        self.data = {
            "sound_resize": 80,
            "rain_resize": 52,
            "difficulty_resize": 120,
            "resolution_resize": 65,
            "sound_active": WHITE,
            "rain_active": WHITE,
            "resolution_active": WHITE,
            "difficulty_active": WHITE,
        }
        match curr_item_options:
            case 0:
                self.data["difficulty_resize"] = 140
                self.data["difficulty_active"] = SELECTED_COLOR
            case 1:
                self.data["sound_resize"] = 100
                self.data["sound_active"] = SELECTED_COLOR
            case 2:
                self.data["rain_resize"] = 70
                self.data["rain_active"] = SELECTED_COLOR
            case 3:
                self.data["resolution_resize"] = 85
                self.data["resolution_active"] = SELECTED_COLOR

    def text_handling(self):
        font = pygame.font.SysFont("Arial", 40, False)
        self.sound_on_of_text = font.render(
            self.sound_system[self.sound_system_index],  # text
            False,  # AA
            self.data["sound_active"]  # TEXT COLOR
        )
        self.sound_on_of_text_rect = self.sound_on_of_text.get_rect(
            center=(SCREEN_WIDTH / 2 + self.data["sound_resize"], SCREEN_HEIGHT // 1.5)
        )
        self.rain_on_of_text = font.render(
            self.rain_status[self.rain_system_index],
            False,
            self.data["rain_active"]
        )
        self.rain_on_of_text_rect = self.rain_on_of_text.get_rect(
            center=(
                SCREEN_WIDTH / 2 + self.data["rain_resize"],
                SCREEN_HEIGHT // 1.2 - 40)
        )
        self.resolution_text = font.render(
            self.resolution[self.resolution_index],
            False,
            self.data["resolution_active"]
        )
        self.resolution_text_rect = self.resolution_text.get_rect(
            center=(SCREEN_WIDTH / 1.8 + self.data["resolution_resize"],
                    SCREEN_HEIGHT - 80)
        )

        self.difficulty_text = font.render(
            self.game_modes[self.index_game_mode],
            False,
            self.colors_difficulty[self.index_game_mode]
        )
        self.difficulty_text_rect = self.difficulty_text.get_rect(
            center=(SCREEN_WIDTH / 2 + self.data["difficulty_resize"],
                    SCREEN_HEIGHT // 1.8)
        )

    def draw_options(self):
        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(self.options_img, (-90, 0))
        for i, opt_item in enumerate(self.options_items):
            if i == self.curr_options_items:
                color = SELECTED_COLOR
                arrows = "X "
                italic = True
            else:
                color = WHITE
                arrows = ""
                italic = False
                self.risize_text = 80
            add_more_spaces = ""
            if i in {3, 0}:
                add_more_spaces = " " * 9
            font = pygame.font.SysFont("Arial", 40, False, italic)
            options_text = font.render(
                arrows + opt_item + " <    " + add_more_spaces + "    >",
                False,
                color)
            options_text_rect = options_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8 + (i * 80))
            )
            self.display_surface.blit(options_text, options_text_rect)
        # calling method to resize the text
        self.resize_text(self.curr_options_items)
        # setting up text informations
        self.text_handling()
        # drawing options text
        self.display_surface.blit(self.difficulty_text, self.difficulty_text_rect)
        self.display_surface.blit(self.sound_on_of_text, self.sound_on_of_text_rect)
        self.display_surface.blit(self.rain_on_of_text, self.rain_on_of_text_rect)
        self.display_surface.blit(self.resolution_text, self.resolution_text_rect)
        self.options_transtion()
        
    def render_fps(self,isfps):
        if isfps == "ON":
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(), 1)), False, WHITE)
            self.display_surface.blit(self.fps_txt, (0, 0))

    def run(self):
        self.running = True
        while self.running:
            self.inputs()
            self.draw_options()
            self.render_fps(self.rain_status[self.rain_system_index])
            main_clock.tick()
            pygame.display.update()
