import os, signal, time
import topics, questions, sounds, ui, display
from datetime import datetime

curdir = os.path.dirname(os.path.realpath(__file__))
topics = topics.Topics(curdir)
bank   = questions.QuestionBank(curdir,
                               topics.topic_directory_name,
                               topics.current_topic_directory(),
                               topics.topic_sound_file_name)
sounds = sounds.Sounds(curdir)
screen = display.Display(curdir)
ui     = ui.UserInterface(topics=topics, question_bank=bank, sounds=sounds, display=screen)

# the entry point to the application...
if __name__ == "__main__":
   signal.signal(signal.SIGINT, ui.cleanup)
   while ui.running:
      time.sleep(0.5)
