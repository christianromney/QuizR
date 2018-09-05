import random
# This "module" contains classes that iterate over a sequence in various ways,
# abstracting knowledge of "how" to navigate over a collection from the code
# that just wants the next item.

class LoopingNavigator:
   """Navigates over a sequence in a circular fashion.
      Calling move_next() when at the end of a sequence returns
      to the beginning."""
   def __init__(self, seq):
      self.seq = seq
      self.index = 0

   def move_next(self):
      if self.index + 1 == len(self.seq):
         self.index = 0
      else:
         self.index = self.index + 1

   def get(self):
      return self.seq[self.index]

class RandomNavigator:
   """Navigates over a sequence in a random fashion, ensuring
   no consecutive repetition."""
   def __init__(self, seq):
      self.seq = seq
      self.last = None
      self.current = random.choice(self.seq)

   def move_next(self):
      self.last = self.current
      self.current = random.choice(self.seq)
      while self.current == self.last:
         self.current = random.choice(self.seq)

   def get(self):
      return self.current
