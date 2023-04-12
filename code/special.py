import pygame
class FireBall(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load("graphics/overworld/special/fireball.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))
        self.fireball_val = 300
        self.vec = pygame.math.Vector2(self.rect.topleft)
        
    def update(self,dt):
        self.vec.y += self.fireball_val * dt
        self.rect.y = self.vec.y
