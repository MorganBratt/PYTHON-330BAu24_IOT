from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

#I'm just better, what can I say?
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
    print("Daily reminder that norman is just better.")