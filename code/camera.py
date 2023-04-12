from random import randint
import pygame
class Camera:
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0

    def camera_system(self, dt):
        self.mx, self.my = pygame.mouse.get_pos()
        if self.mx in range(1270, 1280):
            self.camera_x -= (300 * dt)
        if self.mx in range(0, 190):
            self.camera_x += (300 * dt)
        if self.camera_x > 0:
            self.camera_x = 0
        if self.camera_x < -200:
            self.camera_x = -200

    def shake_window(self):
        shake_offset = randint(-7,7)
        self.camera_x += shake_offset