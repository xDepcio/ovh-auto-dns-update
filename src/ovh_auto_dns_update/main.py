"""
First, install the latest release of Python wrapper: $ pip install ovh
"""

from typing import Annotated, List
import ovh
from dotenv import load_dotenv
import os
import typer
import requests

load_dotenv()
app = typer.Typer()

client = ovh.Client(
    endpoint="ovh-eu",  # Endpoint of API OVH (List of available endpoints: https://github.com/ovh/python-ovh#2-configure-your-application)
    application_key=os.getenv("OVH_APPLICATION_KEY"),
    application_secret=os.getenv("OVH_APPLICATION_SECRET"),
    consumer_key=os.getenv("OVH_CONSUMER_KEY"),
)


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


class OVHApiController:

    @staticmethod
    def delete_A_record(domain: str, record_id: str):
        return client.delete(f"/domain/zone/{domain}/record/{record_id}")

    @staticmethod
    def get_A_record_id(domain: str, subdomain: str):
        result = client.get(
            f"/domain/zone/{domain}/record", fieldType="A", subDomain=subdomain
        )
        if type(result) != list:
            raise Exception("Error while fetching A record ID")

        if len(result) == 0:
            return None

        return result[0]

    @staticmethod
    def add_A_record(domain: str, subdomain: str, target: str):
        return client.post(
            f"/domain/zone/{domain}/record/",
            target=target,
            subDomain=subdomain,
            fieldType="A",
        )

    @staticmethod
    def refresh_dns_zone(domain: str):
        return client.post(f"/domain/zone/{domain}/refresh")


@app.command()
def update(
    domain: Annotated[str, typer.Option()],
    subdomains_list: Annotated[
        List[str], typer.Option("--subdomain", "-s", help="Subdomains to update")
    ],
    application_key: Annotated[
        str, typer.Option("--application-key", "-k", help="Application key")
    ],
    application_secret: Annotated[
        str, typer.Option("--application-secret", "-s", help="Application secret")
    ],
    consumer_key: Annotated[
        str, typer.Option("--consumer-key", "-c", help="Consumer key")
    ],
    force: bool = False,
):
    if not AppDirHandler.app_dir_exists():
        AppDirHandler.create_app_dir()
        with open(AppDirHandler.get_prev_ip_file_path(), "w") as f:
            f.write(get_current_ip())

    prev_ip = AppDirHandler.get_prev_ip()
    current_ip = get_current_ip()

    if prev_ip != current_ip or force:
        for subdomain in subdomains_list:
            record_id = OVHApiController.get_A_record_id(domain, subdomain)
            if record_id:
                OVHApiController.delete_A_record(domain, record_id)
            OVHApiController.add_A_record(domain, subdomain, current_ip)
            OVHApiController.refresh_dns_zone(domain)

        with open(AppDirHandler.get_prev_ip_file_path(), "w") as f:
            f.write(current_ip)

        typer.echo("DNS records updated.")
        return

    typer.echo("No changes detected.")


@app.command()
def test():
    record = OVHApiController.get_A_record_id("adrwal.pl", "strapup")
    print(record)
    # print(OVHApiController.delete_A_record("adrwal.pl", None))
    # print(OVHApiController.add_A_record("adrwal.pl", "xd2", "8.8.8.8"))
    OVHApiController.refresh_dns_zone("adrwal.pl")


if __name__ == "__main__":
    app()
