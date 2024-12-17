import network # type: ignore
import socket
from time import sleep
# copy the picozero folder to the root of the Pico
from picozero import pico_temp_sensor, pico_led # type: ignore
import machine # type: ignore
import json
from machine import Pin, I2C, reset # type: ignore
from ssd1306 import SSD1306_I2C # type: ignore


# import creds from creds.json
try:
    with open('creds.json') as f:
        creds = json.load(f)
except FileNotFoundError:
    print("Error: creds.json file not found.")
    machine.reset()  # Reset the microcontroller
except json.JSONDecodeError: # type: ignore
    print("Error: creds.json file is not a valid JSON.")
    machine.reset()  # Reset the microcontroller
else:
    ssid = creds['ssid']
    password = creds['password']
    print(f"Connecting to {ssid}")
    obfuscated_password = '*' * len(password)
    print(f"Using password {obfuscated_password}")


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Server available at http://{ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

def display_wrapped_text(oled, text):
    max_chars_per_line = 16  # Maximum characters per line
    max_lines = 8  # Maximum lines available

    # Split the text into lines
    lines = [text[i:i + max_chars_per_line] for i in range(0, len(text), max_chars_per_line)]
    oled.fill(0) # Clear the display

    for i, line in enumerate(lines[:max_lines]):  # from 0 to max_lines
        oled.text(line, 0, i * 8)  

    oled.show()

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request.split())
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        display_wrapped_text(oled, f"LED is {state}, Temp is {temperature}")
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    serve(connection)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    machine.reset()