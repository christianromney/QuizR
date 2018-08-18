#from EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import pygame
import time
import os
from datetime import datetime
import random, glob, subprocess

QUESTION = 18
ANSWER_A = 23
ANSWER_B = 24
ANSWER_C = 25

correct  = None
question = None
curdir   = os.path.dirname(os.path.realpath(__file__))

def initialize():
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(QUESTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(ANSWER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(ANSWER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(ANSWER_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   random.seed(datetime.now())
   pygame.mixer.init(channels=1)

def as_filename(parts):
   return os.path.sep.join(parts)

def expand_path(path):
   return os.path.realpath(path)

def find_random_question(last_question):
   pattern = as_filename([curdir, "questions", "**", "*.mp3"])
   results = glob.glob(pattern, recursive=True)
   if not results:
      return []
   else:
      question = random.choice(results)
      if last_question and expand_path(question) == expand_path(last_question):
         return find_random_question(last_question)
      else:
         correct = os.path.dirname(question).split(os.path.sep)[-1]
         return [correct, question]

def play_sound(file):
   pygame.mixer.Sound(expand_path(file))
   pygame.mixer.Sound.play(sound)

def play_message(msg):
   play_sound(as_filename([curdir, "messages", msg + ".mp3"]))

def check_answer(correct, given):
   print("pressed %s " % given)
   play_message("correct" if correct == given else "try-again")

def was_pressed(button):
   return not GPIO.input(button)


initialize()
while True:
   if was_pressed(QUESTION):
      correct, question = find_random_question(question)
      play_sound(question)

   if was_pressed(ANSWER_A):
      check_answer(correct, "a")

   if was_pressed(ANSWER_B):
      check_answer(correct, "b")

   if was_pressed(ANSWER_C):
      check_answer(correct, "c")
