from urllib.parse import urljoin

import click
import requests
from requests.exceptions import ConnectionError


@click.command()
@click.pass_obj
def status(server_conf):
    server, disable_ssl = server_conf
    try:
        r = requests.get(urljoin(server, "status"), verify=not disable_ssl)
    except ConnectionError:
        click.echo("Hayhooks server is not responding. To start one, run `hayhooks run`")
        return

    if r.status_code >= 400:
        body = r.json()
        click.echo(f"Hayhooks server is unhealty: [{r.status_code}] {r. json().get('detail')}")
        return

    click.echo("Hayhooks server is up and running.")
    body = r.json()
    if pipes := body.get("pipelines"):
        click.echo("\nPipelines deployed:")
        for p in pipes:
            click.echo(f"- {p}")
