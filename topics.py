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

    def current_topic_display_name(self):
        """Extracts the current topic's name for textual display."""
        topic = self.current_topic.split(os.path.sep)[-1]
        return string.capwords(topic.replace("-", " "))
