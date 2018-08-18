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
   pygame.mixer.init()

def find_random_question():
   pattern = os.path.sep.join([curdir, "questions", "**", "*.mp3"])
   results = glob.glob(pattern, recursive=True)
   if not results:
      return []
   else:
      question = random.choice(results)
      correct = os.path.dirname(question).split(os.path.sep)[-1]
      return [correct, question]

def play_sound(file):
   pygame.mixer.music.stop()
   time.sleep(0.2)
   pygame.mixer.music.load(os.path.realpath(file))
   pygame.mixer.music.play()

def was_pressed(button):
   return not GPIO.input(button)

def play_message(msg):
   file = os.path.sep.join([curdir, "messages", msg + ".mp3"])
   play_sound(file)

def check_answer(correct, given):
   play_message("correct" if correct == given else "try-again")

initialize()
while True:
   if was_pressed(QUESTION):
      correct, question = find_random_question()
      play_sound(question)

   if was_pressed(ANSWER_A):
      check_answer(correct, "a")

   if was_pressed(ANSWER_B):
      check_answer(correct, "b")

   if was_pressed(ANSWER_C):
      check_answer(correct, "c")
