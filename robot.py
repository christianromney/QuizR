import RPi.GPIO as GPIO
import pygame
import time
import os
import string
import signal
from datetime import datetime
import random, glob, subprocess

TOPIC    = 17
QUESTION = 18
ANSWER_A = 23
ANSWER_B = 24
ANSWER_C = 25
ANSWER_FOLDER = {ANSWER_A: "a",
                 ANSWER_B: "b",
                 ANSWER_C: "c"}

correct  = None
question = None
curdir   = os.path.dirname(os.path.realpath(__file__))

keep_running      = True
exiting           = False
topic_filename    = "topic.mp3"
current_topic_idx = 0
current_topic_dir = None

def as_filename(parts):
   return os.path.sep.join(parts)

def expand_path(path):
   return os.path.realpath(path)

def play_sound(file):
   pygame.mixer.music.load(expand_path(file))
   pygame.mixer.music.play()

def topic_name(path):
   topic = path.split(os.path.sep)[-1]
   return string.capwords(topic.replace("-", " "))

def load_topics():
   pattern = as_filename([curdir, "questions", "*"])
   results = [d for d in glob.glob(pattern) if os.path.isdir(d)]
   print([topic_name(t) for t in results])
   return results

def find_random_question(last_question):
   pattern = as_filename([curdir, "questions", "**", "*.mp3"])
   results = [x for x in glob.glob(pattern, recursive=True) if not x.endswith(topic_filename)]
   if not results:
      return []
   else:
      question = random.choice(results)
      if last_question and expand_path(question) == expand_path(last_question):
         return find_random_question(last_question)
      else:
         correct = os.path.dirname(question).split(os.path.sep)[-1]
         return [correct.lower(), question]

def play_message(msg):
   play_sound(as_filename([curdir, "messages", msg + ".mp3"]))

def check_answer(correct, given):
   print("Selected %s (%s is correct)." % (given, correct))
   play_message("correct" if correct == given else "try-again")

def on_question_button_pressed(channel):
   global correct
   global question
   correct, question = find_random_question(question)
   play_sound(question)

def on_answer_button_pressed(channel):
   global correct
   return check_answer(correct, ANSWER_FOLDER.get(channel).lower())

def on_exit(signal, frame):
   global keep_running
   global exiting
   if not exiting:
      exiting = True
      print("\n\nInterrupt singal received.\nCleaning up GPIO.\nGoodbye!\n\n")
      GPIO.cleanup([QUESTION, ANSWER_A, ANSWER_B, ANSWER_C])
      keep_running = False

def initialize():
   # setup GPIO pin interrupt handlers
   print("Initializing GPIO.")
   GPIO.setmode(GPIO.BCM)

   GPIO.setup(QUESTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(ANSWER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(ANSWER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   GPIO.setup(ANSWER_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   GPIO.add_event_detect(QUESTION, GPIO.FALLING, callback=on_question_button_pressed, bouncetime=300)
   GPIO.add_event_detect(ANSWER_A, GPIO.FALLING, callback=on_answer_button_pressed, bouncetime=300)
   GPIO.add_event_detect(ANSWER_B, GPIO.FALLING, callback=on_answer_button_pressed, bouncetime=300)
   GPIO.add_event_detect(ANSWER_C, GPIO.FALLING, callback=on_answer_button_pressed, bouncetime=300)

   # setup interrupt signal handler (CTRL+C)
   signal.signal(signal.SIGINT, on_exit)

   # initialize data, libraries
   random.seed(datetime.now())
   pygame.mixer.init(channels=1)
   load_topics()

initialize()

while keep_running:
   # the main program loop doesn't do anything interesting
   time.sleep(0.333)
