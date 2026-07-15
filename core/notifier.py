from urllib.parse import quote

import requests

import os

PHONE = os.getenv("PHONE")
APIKEY = os.getenv("APIKEY")

def send_whatsapp(message):

    if not PHONE:
        raise RuntimeError("Environment variable PHONE is not defined")
    
    if not APIKEY:
        raise RuntimeError("Environment variable APIKEY is not defined")

    url = (
        "https://api.callmebot.com/whatsapp.php"
        f"?phone={PHONE}"
        f"&text={quote(message)}"
        f"&apikey={APIKEY}"
    )

    response = requests.get(url)

    response.raise_for_status()
