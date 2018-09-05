import os, random
import RPi.GPIO as GPIO
from datetime import datetime

QUESTION = 18
ANSWER_A = 23
ANSWER_B = 24
ANSWER_C = 25
CHANNELS = [QUESTION, ANSWER_A, ANSWER_B, ANSWER_C]

ANSWER_FROM_CHANNEL = {ANSWER_A: "a",
                       ANSWER_B: "b",
                       ANSWER_C: "c"}

class UserInterface:
    """This is the main application class which wires up the user interface to
    GPIO pins and handles events."""
    def __init__(self, question_bank, sounds):
        """Setting up the GPIO pins with a pull-up resistor means the wire to the GPIO
         pins will be high. therefore, the non-GPIO wire on the switch must go to ground."""
        random.seed(datetime.now())

        self.running       = True
        self.exiting       = False

        self.bank          = question_bank
        self.sounds        = sounds

        print("Initializing GPIO pins with pull-up resistors.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CHANNELS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # setup GPIO pin interrupt handlers
        GPIO.add_event_detect(QUESTION, GPIO.FALLING, callback=self.on_next_button_pressed,   bouncetime=300)
        GPIO.add_event_detect(ANSWER_A, GPIO.FALLING, callback=self.on_answer_button_pressed, bouncetime=300)
        GPIO.add_event_detect(ANSWER_B, GPIO.FALLING, callback=self.on_answer_button_pressed, bouncetime=300)
        GPIO.add_event_detect(ANSWER_C, GPIO.FALLING, callback=self.on_answer_button_pressed, bouncetime=300)

    def determine_answer_from_channel(self, channel):
        """Given a GPIO channel (pin number), returns the associated logical answer (a, b, c)"""
        return ANSWER_FROM_CHANNEL.get(channel)

    def on_next_button_pressed(self, channel):
        """Event handler for the next button."""
        self.bank.next_question()
        self.sounds.play_sound(self.bank.current_question)

    def on_answer_button_pressed(self, channel):
        """Event handler for answer buttons."""
        answer = self.determine_answer_from_channel(channel)
        print("Selected %s (%s is correct)." % (answer, self.bank.correct_answer))
        if self.bank.correct_answer:
            self.sounds.play_message("correct" if self.bank.is_correct(answer) else "incorrect")
        else:
            self.sounds.play_message("question")

    def cleanup(self, _signal, _frame):
        """Handler for application exit. Cleans up GPIO."""
        if not self.exiting:
            self.exiting = True
            print("\n\nInterrupt singal received.\nCleaning up GPIO.\nGoodbye!\n\n")
            GPIO.cleanup(CHANNELS)
            self.running = False
