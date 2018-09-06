import os, random, glob, string, signal
import navigation

class Topics:
    """WIP: This class will eventually manage topic navigation and selection."""
    def __init__(self, base_path):
        self.base_path = base_path
        self.topic_directory_name = "questions"
        self.topic_file_name = "topic.mp3"

        pattern = os.path.sep.join([base_path, self.topic_directory_name, "*"])

        self.topics = [d for d in glob.glob(pattern) if os.path.isdir(d)]
        self.navigator = navigation.LoopingNavigator(self.topics)
        self.current_topic = self.navigator.get()

    def next_topic(self):
        self.navigator.move_next()
        self.current_topic = self.navigator.get()

    def current_topic_sound_file(self):
        return self.current_topic + os.path.sep + self.topic_file_name

    def current_topic_directory(self):
        return self.current_topic.split(os.path.sep)[-1]

    def current_topic_display_name(self):
        return string.capwords(self.current_topic_directory().replace("-", " "))
