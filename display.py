import os
from luma.core.interface.serial import i2c, noop
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.emulator.device import pygame, capture, gifanim
from luma.core.error import DeviceNotFoundError
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT, TINY_FONT, LCD_FONT

class Display:
    def __init__(self):
        try:
            self.serial = i2c(port=1, address=0x3C)
            self.device = ssd1306(self.serial, height=32)
        except DeviceNotFoundError:
            self.serial = noop()
            self.device = capture(height=32)

    def text(self, message):
        print("Displaying: %s" % message)
        show_message(self.device,
                     message,
                     y_offset=10,
                     scroll_delay=0.03,
                     font=proportional(SINCLAIR_FONT))

    def file(self, path):
        with open(path, "r") as f:
            self.text(f.read().capitalize())
