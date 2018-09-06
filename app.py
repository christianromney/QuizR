import os, signal, time
import topics, questions, sounds, ui
from datetime import datetime

curdir  = os.path.dirname(os.path.realpath(__file__))
topics  = topics.Topics(curdir)
bank    = questions.QuestionBank(curdir,
                                topics.topic_directory_name,
                                topics.current_topic_directory(),
                                topics.topic_sound_file_name)
sounds  = sounds.Sounds(curdir)
ui      = ui.UserInterface(topics, bank, sounds)

# the entry point to the application...
if __name__ == "__main__":
   signal.signal(signal.SIGINT, ui.cleanup)
   while ui.running:
      time.sleep(0.5)
