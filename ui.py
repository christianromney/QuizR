import os, random
import RPi.GPIO as GPIO
from datetime import datetime

TOGGLE   = 17
NEXT     = 18
ANSWER_A = 23
ANSWER_B = 24
ANSWER_C = 25
CHANNELS = [NEXT, ANSWER_A, ANSWER_B, ANSWER_C]

ANSWER_FROM_CHANNEL = {ANSWER_A: "a",
                       ANSWER_B: "b",
                       ANSWER_C: "c"}

class UserInterface:
    """This is the main application class which wires up the user interface to
    GPIO pins and handles events."""
    def __init__(self, topics=None, question_bank=None, sounds=None, display=None, debounce=1000):
        """Setting up the GPIO pins with a pull-up resistor means the wire to the GPIO
         pins will be high. therefore, the non-GPIO wire on the switch must go to ground."""
        random.seed(datetime.now())

        self.running = True
        self.exiting = False

        self.topics  = topics
        self.bank    = question_bank
        self.sounds  = sounds
        self.display = display

        print("Initializing GPIO pins with pull-up resistors.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(CHANNELS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # setup GPIO pin interrupt handlers
        GPIO.add_event_detect(NEXT,     GPIO.FALLING, callback=self.on_next_button_pressed,   bouncetime=debounce)
        GPIO.add_event_detect(ANSWER_A, GPIO.FALLING, callback=self.on_answer_button_pressed, bouncetime=debounce)
        GPIO.add_event_detect(ANSWER_B, GPIO.FALLING, callback=self.on_answer_button_pressed, bouncetime=debounce)
        GPIO.add_event_detect(ANSWER_C, GPIO.FALLING, callback=self.on_answer_button_pressed, bouncetime=debounce)

        self.sounds.play_message("startup")
        self.display.file(self.topics.current_topic_text_file(), capitalize=True)

    def determine_answer_from_channel(self, channel):
        """Given a GPIO channel (pin number), returns the associated logical answer (a, b, c)"""
        return ANSWER_FROM_CHANNEL.get(channel)

    def on_next_button_pressed(self, channel):
        """Event handler for the next button."""
        print("\nNext button pressed")
        if GPIO.input(TOGGLE):
            self.topics.next_topic()
            self.bank.reset_topic_questions(self.topics.current_topic_directory())
            self.sounds.play_sound(self.topics.current_topic_sound_file())
            self.display.file(self.topics.current_topic_text_file(), capitalize=True)
        else:
            self.bank.next_question()
            self.sounds.play_sound(self.bank.current_question)
            self.display.file(self.bank.current_question_text_file())

    def on_answer_button_pressed(self, channel):
        """Event handler for answer buttons."""
        self.display.clear()
        answer = self.determine_answer_from_channel(channel)
        print("Selected %s (%s is correct)." % (answer, self.bank.correct_answer))
        if self.bank.correct_answer:
            if self.bank.is_correct(answer):
                self.sounds.play_message("correct")
                self.display.text("Correct!")
            else:
                self.sounds.play_message("incorrect")
                self.display.text("Incorrect...")
        else:
            self.sounds.play_message("question")

    def cleanup(self, _signal, _frame):
        """Handler for application exit. Cleans up GPIO."""
        if not self.exiting:
            self.exiting = True
            print("\n\nInterrupt singal received.\nCleaning up GPIO.\nGoodbye!\n\n")
            GPIO.cleanup(CHANNELS)
            self.display.cleanup()
            self.running = False
