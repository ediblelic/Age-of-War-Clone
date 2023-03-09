import pygame


class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.music_on = False
        self.bg_music = pygame.mixer.Sound("audio/bg_sound.mp3")
        self.bg_music.set_volume(0.5)
        # -1 means the sound will play indefinitely

    #    self.sound_effects = {
    #       "gunshot": pygame.mixer.Sound("gunshot.ogg"),
    #      "explosion": pygame.mixer.Sound("explosion.ogg")
    # }
    # for sound in self.sound_effects.values():
    #   sound.set_volume(0.5)
    def play_effect(self, effect_name):
        self.sound_effects[effect_name].play()

    def toggle_bg_music_on(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.bg_music.play()
        else:
            self.bg_music.stop()

# def set_effect_volume(self, volume):
#    for sound in self.sound_effects.values():
#       sound.set_volume(volume)

# def set_bg_music_volume(self, volume):
#   self.bg_music.set_volume(volume)
