#from EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import time
import os
from datetime import datetime
import random, glob, subprocess

QUESTION = 18
ANSWER_A = 23
ANSWER_B = 24
ANSWER_C = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(QUESTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ANSWER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ANSWER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ANSWER_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_robot = None
previous_human = None
curdir = os.path.dirname(os.path.realpath(__file__))
random.seed(datetime.now())

def find_random_question():
   pattern = os.path.sep.join([curdir, "questions", "**", "*.mp3"])
   results = glob.glob(pattern, recursive=True)
   if not results:
      return []
   else:
      question = random.choice(results)
      correct = os.path.dirname(question).split(os.path.sep)[-1]
      return [correct, os.path.realpath(question)]

def play_sound(file):
   time.sleep(0.2)
   os.system ('mpg123 ' + file)

def was_pressed(button):
   return not GPIO.input(button)

while True:
    if was_pressed(QUESTION):
       correct, question = find_random_question()
       play_sound(question)

    # if was_pressed(ANSWER_A):
    #     previous_robot = button_pressed('robot', previous_robot)

    # if was_pressed(ANSWER_B):
    #     previous_human = button_pressed('human', previous_robot)

    # if was_pressed(ANSWER_C):
    #     previous_robot = button_pressed('robot', previous_robot)

GPIO.cleanup()
