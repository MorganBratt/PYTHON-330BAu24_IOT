# PYTHON-330BAu24_IOT
IOT project for Python 330B 


# Goal
My goal was to get a new Raspberry Pi Pico 2 W and setup a simple web server that would take text input and display it on a screen.  I also wanted to see if I could use Visual Studo Code for this instead of Thonny.


# Hardware
I purchased the following:
- [Raspberry Pi Pico 2 W](https://www.raspberrypi.com/products/raspberry-pi-pico-2/)
- [A 128x64 Pixel SSD1306 OLED display](https://www.amazon.com/dp/B09T6SJBV5)
- A Large 830 Hole Breadboard
- Set of two 20-pin Headers
- M/M Jumper Wires
- Soldering iron and Solder


# Helpful guides
Capturing the following guides I used to build the project  
https://projects.raspberrypi.org/en/projects/get-started-pico-w/0  
https://github.com/paulober/MicroPico/  
https://how2electronics.com/simple-calculator-using-keypad-oled-raspberry-pi-pico/  
https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html  

# Imported Modules
[micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306)  
[picozero](https://github.com/RaspberryPiFoundation/picozero)  

# Wirinng
| Pico Pin | ssd1306 Pin |
| -------- | ----------- | 
| GP0\SDA  | SDA |
| GP1\SCL  | SCL | 
| GP38\Ground  |GND |
| GP36\3v3 Out | VCC | 

# Program Flow
1) After startup the Pico will connect to wireless and serve a basic web page
    ![](https://gist.githubusercontent.com/MorganBratt/b3ceffedc0d0f072143e70fe46ed0904/raw/55f0a68e2f6280f35351c0bd4c8c2f17965c215c/PXL_20241217_013706859.jpg)
2) The user can connect to the device and submit a string of 96 characters to display on the screen connected to the Pico  
    ![](https://gist.githubusercontent.com/MorganBratt/b3ceffedc0d0f072143e70fe46ed0904/raw/55f0a68e2f6280f35351c0bd4c8c2f17965c215c/Screenshot%25202024-12-16%2520175822.png)
3) The simple web server interprets the user input and displays it on the 128x64 screen with a Python image at the bottom right.
    ![](https://gist.githubusercontent.com/MorganBratt/b3ceffedc0d0f072143e70fe46ed0904/raw/55f0a68e2f6280f35351c0bd4c8c2f17965c215c/PXL_20241217_015916918.jpg)





## Example creds.json file
``` json
{
    "ssid": "your_wireless_ssid",
    "password": "your_wireless_password"
}
```

