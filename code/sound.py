import pygame
class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.music_on = False
        self.bg_music = pygame.mixer.Sound("../audio/bg_sound.mp3")
        self.bg_music.set_volume(0.5)

        self.sound_effects = {
           "fireball": pygame.mixer.Sound("../audio/effects/special.wav"),
           "add_coin": pygame.mixer.Sound("../audio/effects/coin.wav"),
           "catapult": pygame.mixer.Sound("../audio/effects/catapult.wav")
        }
        self.set_effect_volume(0.1)


    def play_effect(self, effect_name):
        self.sound_effects[effect_name].play()

    def toggle_bg_music_on(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.bg_music.play()
        else:
            self.bg_music.stop()

    def set_effect_volume(self, volume: float):
        for sound in self.sound_effects.values():
            sound.set_volume(volume)
