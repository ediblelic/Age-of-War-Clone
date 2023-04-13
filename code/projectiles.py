import pygame


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(
            "../graphics/player_animations/archer/attack/arrow.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.demage = 1
        self.velocity = 100
        self.vec_direction = pygame.math.Vector2(self.rect.topleft)

    def launch(self, dt, enemy):
        self.vec_direction.x += self.velocity * dt * enemy
        self.rect.x = self.vec_direction.x


class CatapultProjectil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(
            "../graphics/overworld/ui/miniguns/projectile.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.damage = 500
        self.velocity = 100
        self.vec_direction = pygame.math.Vector2(self.rect.topleft)
        self.delay = 10

    def launch(self, dt, angle, isenemy):
        self.vec_direction.x += self.velocity * dt * isenemy
        self.vec_direction.y += angle * dt
        self.rect.x = self.vec_direction.x
        self.rect.y = self.vec_direction.y
