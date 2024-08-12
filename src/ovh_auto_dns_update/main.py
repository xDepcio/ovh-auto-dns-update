"""
First, install the latest release of Python wrapper: $ pip install ovh
"""

from typing import Annotated, List
import ovh
import typer

from ovh_auto_dns_update.api_contoller import OVHApiController
from ovh_auto_dns_update.app_dir_handler import AppDirHandler
from ovh_auto_dns_update.utils import get_current_ip

app = typer.Typer()


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
        str, typer.Option("--application-secret", "-a", help="Application secret")
    ],
    consumer_key: Annotated[
        str, typer.Option("--consumer-key", "-c", help="Consumer key")
    ],
    force: bool = False,
):
    client = ovh.Client(
        endpoint="ovh-eu",
        application_key=application_key,
        application_secret=application_secret,
        consumer_key=consumer_key,
    )

    if not AppDirHandler.app_dir_exists():
        AppDirHandler.create_app_dir()
        with open(AppDirHandler.get_prev_ip_file_path(), "w") as f:
            f.write(get_current_ip())

    prev_ip = AppDirHandler.get_prev_ip()
    current_ip = get_current_ip()

    api_contoller = OVHApiController(client, domain)
    if prev_ip != current_ip or force:
        for subdomain in subdomains_list:
            record_id = api_contoller.get_A_record_id(subdomain)
            if record_id:
                api_contoller.delete_A_record(record_id)
            api_contoller.add_A_record(subdomain, current_ip)
            api_contoller.refresh_dns_zone()

        with open(AppDirHandler.get_prev_ip_file_path(), "w") as f:
            f.write(current_ip)

        typer.echo("DNS records updated.")
        return

    typer.echo("No changes detected.")


@app.command()
def test():
    # record = OVHApiController.get_A_record_id("adrwal.pl", "strapup")
    # print(record)
    # print(OVHApiController.delete_A_record("adrwal.pl", None))
    # print(OVHApiController.add_A_record("adrwal.pl", "xd2", "8.8.8.8"))
    # OVHApiController.refresh_dns_zone("adrwal.pl")
    pass


if __name__ == "__main__":
    app()
