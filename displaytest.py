from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)


while True:
    oled.fill(0)
    oled.text("Hi Norman!", 0, 0)
    oled.show()
    sleep(1)
    oled.fill(0)
    oled.text("Norman is better", 0, 0)
    oled.text("than Liam", 0, 8)
    oled.show()
    sleep(1)
    print("looping")