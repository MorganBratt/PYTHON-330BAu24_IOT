import network  # type: ignore
import socket
from time import sleep
import machine  # type: ignore
import json
from machine import Pin, I2C, reset  # type: ignore
from ssd1306 import SSD1306_I2C  # type: ignore

# import creds from creds.json
try:
    with open("creds.json") as f:
        creds = json.load(f)
except FileNotFoundError:
    print("Error: creds.json file not found.")
    machine.reset()  # Reset the microcontroller
except json.JSONDecodeError:
    print("Error: creds.json file is not a valid JSON.")
    machine.reset()  # Reset the microcontroller
else:
    ssid = creds["ssid"]
    password = creds["password"]
    print(f"Connecting to {ssid}")
    obfuscated_password = "*" * len(password)
    print(f"Using password {obfuscated_password}")


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Server available at http://{ip}")
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage():
    # Template HTML
    html = """
            <!DOCTYPE html>
            <html>
            <form action="/submit" method="post">
            <label for="text">Enter text (max 128 characters):</label><br>
            <input type="text" id="text" name="text" maxlength="128" pattern="[ -~]*" required><br>
            <input type="submit" value="Submit">
            </form>
            </body>
            </html>
            """
    return str(html)


def display_wrapped_text(oled, text):
    max_chars_per_line = 16  # Maximum characters per line
    max_lines = 8  # Maximum lines available

    # Decode URL-encoded characters manually
    print(text)
    decoded_text = (
        text.replace("%20", " ")
        .replace("%21", "!")
        .replace("%22", '"')
        .replace("%23", "#")
        .replace("%24", "$")
        .replace("%25", "%")
        .replace("%26", "&")
        .replace("%27", "'")
        .replace("%28", "(")
        .replace("%29", ")")
        .replace("%2A", "*")
        .replace("%2B", "+")
        .replace("%2C", ",")
        .replace("%2D", "-")
        .replace("%2E", ".")
        .replace("%2F", "/")
        .replace("%3A", ":")
        .replace("%3B", ";")
        .replace("%3C", "<")
        .replace("%3D", "=")
        .replace("%3E", ">")
        .replace("%3F", "?")
        .replace("%40", "@")
        .replace("%5B", "[")
        .replace("%5C", "\\")
        .replace("%5D", "]")
        .replace("%5E", "^")
        .replace("%5F", "_")
        .replace("%60", "`")
        .replace("%7B", "{")
        .replace("%7C", "|")
        .replace("%7D", "}")
        .replace("%7E", "~")
    )

    # Split the text into lines
    lines = [
        decoded_text[i : i + max_chars_per_line]
        for i in range(0, len(decoded_text), max_chars_per_line)
    ]
    oled.fill(0)  # Clear the display

    for i, line in enumerate(lines[:max_lines]):  # from 0 to max_lines
        oled.text(line, 0, i * 8)

    oled.show()


def serve(connection, ip):
    # Start a web server
    display_wrapped_text(oled, f"Server running at http://{ip}")

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request_path = request.split()[1]
        except IndexError:
            pass

        if request_path == "/submit":
            # Extract the user string from the request body
            request_body = request.split("\\r\\n\\r\\n")[
                1
            ]  # find the double newline where the body is
            user_string = request_body.split("=")[1]
            user_string = user_string.replace("+", " ")  # Replace '+' with space
            if user_string.endswith("'"):  # Remove trailing single quote if present
                user_string = user_string[:-1]
            display_wrapped_text(oled, user_string)

        html = webpage()
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    serve(connection, ip)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    machine.reset()
