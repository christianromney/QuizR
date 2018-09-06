import os, random, glob
import navigation

class QuestionBank:
   """This class manages question navigation and checking the correctness of
answers.
   """
   def __init__(self, base_path, topic_directory, topic_name, ignore_suffix):
      self.current_question = None
      self.correct_answer   = None
      self.ignore           = ignore_suffix
      self.base_path        = base_path
      self.topic_directory  = topic_directory
      self.reset_topic_questions(topic_name)

   def reset_topic_questions(self, topic_name):
      pattern        = os.path.sep.join([self.base_path, self.topic_directory, topic_name, "**", "*.mp3"])
      self.questions = [x for x in glob.glob(pattern, recursive=True) if not x.endswith(self.ignore)]
      self.navigator = navigation.RandomNavigator(self.questions)

   def next_question(self):
      """Randomly selects the next question (using the navigator module)."""
      if self.questions:
         self.current_question = self.navigator.get()
         self.correct_answer   = os.path.dirname(self.current_question).split(os.path.sep)[-1].lower()
         self.navigator.move_next()

   def is_correct(self, answer):
      """Validates the correctness of the given answer."""
      return self.correct_answer.lower() == answer.lower()
