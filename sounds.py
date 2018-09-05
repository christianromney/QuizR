import os, glob, random, pygame

class Sounds:
    """This class manages sound playback."""
    def __init__(self, base_path):
        pygame.mixer.init(channels=1)
        self.sound_resource_path = base_path

    def play_sound(self, file):
        pygame.mixer.music.load(os.path.realpath(file))
        pygame.mixer.music.play()

    def play_message(self, msg_type):
        pattern = os.path.sep.join([self.sound_resource_path, "messages", msg_type, "*.mp3"])
        self.play_sound(random.choice(glob.glob(pattern)))
