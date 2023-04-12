import pygame
class Building(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.surface.Surface((100,100))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(pos_x,pos_y))

        
    def building_collision(self,dt):
        player_building = self.player_building.sprites()[0]
        enemy_building = self.enemy_building.sprites()[0]
        if not self.player_units:
            for enemy in self.enemy_units:
                if enemy.rect.colliderect(player_building.rect):
                    enemy.attack(dt,-1)
                    self.ui.player_hp -= 0.1
        elif not self.enemy_units:
            for player in self.player_units:
                if player.rect.colliderect(enemy_building.rect):
                    self.ui.enemy_hp -= 0.1
                    player.attack(dt,1)