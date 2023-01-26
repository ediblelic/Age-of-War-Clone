import pygame
from settings import *
class Introduction:
    def __init__(self):
        self.my_font = pygame.font.SysFont("Arial", 20)
        pygame.mouse.set_visible(False)
        self.display_surface = pygame.display.get_surface()
        self.running = True
        self.transtion_step = 2
        self.transtion = True
        self.story_images = []
        self.setting_story_images()
        self.timer = 0
    def setting_story_images(self):
        for x in range(4):
            self.story_images.append(pygame.image.load(f"graphics/overworld/story{x}.jpg").convert())
            self.story_images[x].set_alpha(0)     
    def loading_story(self):
        self.timer += 0.0010
        for i in range(4):
            if  i == 0:
                self.transtions(i)
                self.display_surface.blit(self.story_images[i],(0,0))
            elif self.timer > 2 and i == 1:
                self.transtions(i)
                self.display_surface.blit(self.story_images[i],(0,0))
            elif self.timer > 4 and i == 2 :
                self.transtions(i)
                self.display_surface.blit(self.story_images[i],(0,0))
            elif self.timer > 5 and i == 3:
                self.transtions(i)
                self.display_surface.blit(self.story_images[i],(0,0))
        if self.timer > 7:
                self.running = False
    def transtions(self,i: int):
        if self.transtion:
            self.story_images[i].set_alpha(self.story_images[i].get_alpha() + self.transtion_step)
    def run_story(self):
        while self.running:
            self.fps_txt = self.my_font.render("Fps:" + str(round(main_clock.get_fps(),1)),False,(255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display_surface.fill((0,0,0))
            self.loading_story()
            self.current_time = pygame.time.get_ticks()
            self.display_surface.blit(self.fps_txt,(0,0))
            pygame.display.update()
            main_clock.tick()