from machine import Pin, I2C, reset # type: ignore
from ssd1306 import SSD1306_I2C # type: ignore
from time import sleep
import os


i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# for text 8 lines of 16 characters
# 128 total characters
print(os.listdir())

def display_wrapped_text(oled, text):
    max_chars_per_line = 16  # Maximum characters per line
    max_lines = 8  # Maximum lines available

    # Split the text into lines
    lines = [text[i:i + max_chars_per_line] for i in range(0, len(text), max_chars_per_line)]
    oled.fill(0) # Clear the display

    for i, line in enumerate(lines[:max_lines]):  # from 0 to max_lines
        oled.text(line, 0, i * 8)  

    oled.show()


#I'm just better, what can I say?
try:
    while True:
        oled.fill(0)
        oled.text("Hi Dad!", 0, 0)
        oled.show()
        sleep(1)
        oled.fill(0)
        oled.fill_rect(0, 0, 8, 8, 1)
        oled.fill_rect(24, 0, 8, 8, 1)
        oled.fill_rect(0, 16, 8, 8, 1)
        oled.fill_rect(8, 24, 8, 8, 1)
        oled.fill_rect(16, 24, 8, 8, 1)
        oled.fill_rect(24, 16, 8, 8, 1)
        oled.text("I'm just better", 0, 40)
        oled.show()
        sleep(1)
        oled.fill(0)
        oled.fill_rect(8, 0, 16, 8, 1)
        oled.fill_rect(32, 0, 16, 8, 1)
        oled.fill_rect(0, 8, 56, 16, 1)
        oled.fill_rect(8, 24, 40, 8, 1)
        oled.fill_rect(16, 32, 24, 8, 1)
        oled.fill_rect(24, 40, 8, 8, 1)
        oled.show()
        sleep(1)
        display_wrapped_text(oled, "This is a really long string of text that should wrap automatically.")
        sleep(10)
        print("Daily reminder that norman is just better.")
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    reset()
