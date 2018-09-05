import os, random, glob
import navigation

class QuestionBank:
   """This class manages question navigation and checking the correctness of
answers.
   """
   def __init__(self, base_path, topic_directory_name, ignore_suffix):
      pattern = os.path.sep.join([base_path, topic_directory_name, "**", "*.mp3"])
      self.current_question = None
      self.correct_answer   = None
      self.questions        = [x for x in glob.glob(pattern, recursive=True) if not x.endswith(ignore_suffix)]
      self.navigator        = navigation.RandomNavigator(self.questions)

   def next_question(self):
      """Randomly selects the next question (using the navigator module)."""
      if self.questions:
         self.current_question = self.navigator.get()
         self.correct_answer   = os.path.dirname(self.current_question).split(os.path.sep)[-1].lower()
         self.navigator.move_next()

   def is_correct(self, answer):
      """Validates the correctness of the given answer."""
      return self.correct_answer.lower() == answer.lower()
