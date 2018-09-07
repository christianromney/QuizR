import time, os
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Display:
    def __init__(self, font="RedAlert"):
        path         = self.abspath(os.path.join("fonts", font + ".ttf"))
        self.font    = ImageFont.truetype(path, 20)
        self.device  = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.width   = self.device.width
        self.height  = self.device.height
        self.image   = Image.new('1', (self.width, self.height))
        self.draw    = ImageDraw.Draw(self.image)
        self.device.begin()
        self.device.clear()
        self.device.display()

    def abspath(self, relative):
        return os.path.abspath(os.path.join(os.curdir, relative))

    def text(self, message):
        self.draw.text((2, 8), message, font=self.font, fill=255)
        self.device.image(self.image)
        self.device.display()

    def clear(self):
        self.image   = Image.new('1', (self.width, self.height))
        self.draw    = ImageDraw.Draw(self.image)

    def scroll(self, message, rate=0.3):
        for x in range(len(message) + 1):
            self.text(message[x:] or "")
            time.sleep(rate)
            self.clear()

    def file(self, path):
        with open(path, "r") as f:
            self.scroll(f.read().capitalize())
