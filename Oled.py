#!/usr/bin/python
import board
import os
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from retrying import retry


class Oled:

    def __init__(self, font_size):
        # Setting some variables for our reset pin etc.
        self.RESET_PIN = digitalio.DigitalInOut(board.D4)

        # declare member variables
        self.draw = None
        self.font = None
        self.disp = None
        self.image = None
        self.font_size = font_size

        # Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
        i2c = board.I2C()
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

        # set full puth for incling libs below
        full_path = os.path.dirname(os.path.abspath(__file__)) + "/"

        # Load a font in 2 different sizes.
        self.font = ImageFont.truetype(full_path + '/DejaVuSans.ttf', self.font_size)

    @retry()
    def display(self, text):

        # Create blank image for drawing.
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)

        self.draw.text((0, 0), str(text), font=self.font, fill=255)

        # Clear display.
        self.disp.fill(0)
        self.disp.image(self.image)
        self.disp.show()