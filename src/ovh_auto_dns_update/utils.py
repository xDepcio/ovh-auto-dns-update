import requests


def get_current_ip():
    return requests.get("https://ifconfig.me/").text
