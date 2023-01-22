from settings import *
import pygame
from sound import Sound
class Options:
    def __init__(self):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', 25)
        self.display_surface = pygame.display.get_surface()
        self.rain_status = ["OFF","ON"]
        self.sound_system = ['ON','OFF']
        self.options_items = ["SOUND","RAIN","RESOLUTION"]
        self.resolution = [f"{screen_width}x{screen_heigth}","Fullscreen"]
        self.resolution_index = 0
        self.sound_system_index = 0
        self.rain_system_index = 0
        self.curr_options_items = 0
        self.options_img = pygame.image.load("graphics/main_menu_images/options_img.jpg").convert_alpha()
        self.sound = Sound()
        
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
                if event.key == pygame.K_RIGHT:
                    match self.options_items[self.curr_options_items]:
                        case "SOUND":
                            self.sound.toggle_bg_music_on()
                            self.sound_system_index = (self.sound_system_index + 1) % len(self.sound_system)
                        case "RAIN":
                            self.rain_system_index = (self.rain_system_index + 1) % len(self.rain_status)
                        case "RESOLUTION":
                            self.resolution_index = (self.resolution_index + 1) % len(self.resolution)
                if event.key == pygame.K_LEFT:
                     match self.options_items[self.curr_options_items]:
                        case "SOUND":
                            self.sound.toggle_bg_music_on()
                            self.sound_system_index = (self.sound_system_index - 1) % len(self.sound_system)
                        case "RAIN":
                            self.rain_system_index = (self.rain_system_index - 1) % len(self.rain_status)
                        case "RESOLUTION":
                            self.resolution_index = (self.resolution_index - 1) % len(self.resolution)
                if event.key == pygame.K_RETURN:
                    if self.options_items[self.curr_options_items] == "RESOLUTION" and self.resolution_index == 1:
                        self.display_surface = pygame.display.set_mode((screen_width,screen_heigth),pygame.FULLSCREEN)
                    elif self.options_items[self.curr_options_items] == "RESOLUTION" and self.resolution_index == 0:
                        self.display_surface = pygame.display.set_mode((screen_width,screen_heigth))

    def resize_text(self,curr_item_options):
        self.data = {
            "sound_resize": 80,
            "rain_resize": 52,
            "resolution_resize": 65,
            "sound_active": (255,255,255),
            "rain_active": (255,255,255),
            "resolution_active": (255,255,255)
        }
        match curr_item_options:
            case 0:
                self.data["sound_resize"] = 100
                self.data["sound_active"] = selected_color
            case 1:
                self.data["rain_resize"] = 78
                self.data["rain_active"] = selected_color
            case 2:
                self.data["resolution_resize"] = 85
                self.data["resolution_active"] = selected_color
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
                self.risize_text = 80
            add_more_spaces = ""
            # if we on fullscreen item 
            if i == 2:
                add_more_spaces = " " * 10
            font = pygame.font.SysFont("Arial",40,False,italic)
            options_text = font.render(arrows + opt_item + " <    " +  add_more_spaces + "    >",False,color)
            options_text_rect = options_text.get_rect(center=(screen_width/2,screen_heigth / 1.5 + (i * 100)))
            self.display_surface.blit(options_text,options_text_rect)
        # calling method to resize the text 
        self.resize_text(self.curr_options_items)
        # setting up text informations
        sound_on_of_text = font.render(self.sound_system[self.sound_system_index],False,self.data["sound_active"])
        sound_on_of_text_rect = sound_on_of_text.get_rect(center=(screen_width/2 + self.data["sound_resize"],screen_heigth // 1.5))
        rain_on_of_text = font.render(self.rain_status[self.rain_system_index],False,self.data["rain_active"])
        rain_on_of_text_rect = rain_on_of_text.get_rect(center=(screen_width/2 + self.data["rain_resize"],screen_heigth // 1.2 - 20))
        resolution_text = font.render(self.resolution[self.resolution_index],False,self.data["resolution_active"])
        resolution_text_rect = resolution_text.get_rect(center=(screen_width/1.8 + self.data["resolution_resize"] ,screen_heigth // 1 - 40))
        # drawing options text
        self.display_surface.blit(sound_on_of_text,sound_on_of_text_rect)
        self.display_surface.blit(rain_on_of_text,rain_on_of_text_rect)
        self.display_surface.blit(resolution_text,resolution_text_rect)
    def run(self):
        self.running = True
        while self.running:
            self.inputs()
            self.fps_txt = self.my_font.render(str(round(main_clock.get_fps(),1)),False,(255,255,255))
            self.display_surface.fill((255,0,0))
            self.display_surface.blit(self.options_img,(-90,0))
            self.draw_options()
            self.display_surface.blit(self.fps_txt,(0,0))
            main_clock.tick()
            pygame.display.update()
