"""
First, install the latest release of Python wrapper: $ pip install ovh
"""

from dataclasses import dataclass
import json
from typing import Annotated, List
import ovh
from dotenv import load_dotenv
import os
import typer
import requests

load_dotenv()
app = typer.Typer()
# Instantiate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page (https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*)
client = ovh.Client(
    endpoint="ovh-eu",  # Endpoint of API OVH (List of available endpoints: https://github.com/ovh/python-ovh#2-configure-your-application)
    application_key=os.getenv("OVH_APPLICATION_KEY"),
    application_secret=os.getenv("OVH_APPLICATION_SECRET"),
    consumer_key=os.getenv("OVH_CONSUMER_KEY"),
)

result = client.get("/domain")

# Pretty print
print(json.dumps(result, indent=4))

result2 = client.get("/domain/zone/adrwal.pl/record/")
print(json.dumps(result2, indent=4))

result3 = client.get("/domain/zone/adrwal.pl/record/5316053875/")
print(json.dumps(result3, indent=4))

# postResult = client.post("/domain/zone/adrwal.pl/record/", target="8.8.8.8", subDomain="olek-test", fieldType='A')

# print(json.dumps(postResult, indent=4))

# refreshResult = client.post("/domain/zone/adrwal.pl/refresh")

# # Pretty print
# print(json.dumps(refreshResult, indent=4))

resultRecords = client.get(
    "/domain/zone/adrwal.pl/record", fieldType="A", subDomain="strapup"
)


@dataclass
class Config:
    domain: str
    subdomains: list[str]


# Pretty print
print(json.dumps(resultRecords, indent=4))


def get_current_ip():
    return requests.get("https://ifconfig.me/").text


class AppDirHandler:

    @staticmethod
    def create_app_dir():
        os.makedirs(os.path.expanduser("~/.ovh_auto_dns_update"))
        ip_file_path = os.path.expanduser("~/.ovh_auto_dns_update/prev-ip.txt")
        with open(ip_file_path, "w") as f:
            f.write("")

    @staticmethod
    def app_dir_exists():
        return os.path.exists(os.path.expanduser("~/.ovh_auto_dns_update"))

    @staticmethod
    def get_app_dir_path():
        return os.path.expanduser("~/.ovh_auto_dns_update")

    @staticmethod
    def get_prev_ip_file_path():
        return os.path.join(AppDirHandler.get_app_dir_path(), "prev-ip.txt")

    @staticmethod
    def get_prev_ip():
        with open(AppDirHandler.get_prev_ip_file_path(), "r") as f:
            return f.read()


@app.command()
def update(
    domain: Annotated[str, typer.Option()],
    subdomain: Annotated[List[str], typer.Option()],
    force: bool = False,
):
    if not AppDirHandler.app_dir_exists():
        AppDirHandler.create_app_dir()
        with open(AppDirHandler.get_prev_ip_file_path(), "w") as f:
            f.write(get_current_ip())

    prev_ip = AppDirHandler.get_prev_ip()
    current_ip = get_current_ip()


if __name__ == "__main__":
    app()
