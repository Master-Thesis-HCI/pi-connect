import os
import subprocess
import requests
import pathlib
import socket
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


TOKEN = pathlib.Path('/home/pi/pi-connect/.token').read_text().strip()
DESTINATION_URL = "https://pi.romanpeters.nl/"


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_ssid() -> str:
    try:
        output = subprocess.check_output(['iwgetid'])
        return output.split('"')[1]
    except Exception as e:
        logger.warning(e)
    return ""

def gen_payload() -> dict:
    payload = {}
    payload['hostname'] = socket.gethostname()
    payload['ip'] = get_ip()
    payload['ssid'] = get_ssid()
    return payload

def broadcast(payload):
    headers = {"Content-Type": "application/json",
               "Authorization": TOKEN}
    res = requests.post(DESTINATION_URL, json=payload, headers=headers)
    if res.status_code != 200:
        logger.exception('Broadcast failed')



if __name__=="__main__":
    payload = gen_payload()
    broadcast(payload)
    print("Completed")
