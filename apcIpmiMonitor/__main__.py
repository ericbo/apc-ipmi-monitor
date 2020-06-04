import importlib
import sys

import click

# Add apcIpmiMpnitor to dev workspace
if not importlib.util.find_spec("apcIpmiMonitor"):
    sys.path.insert(0, ".")

from apcIpmiMonitor.Infrastructure.ApcGateway import ApcGateway
from apcIpmiMonitor.Config import Config
from apcIpmiMonitor.Infrastructure.IpmiGateway import IpmiGateway
from apcIpmiMonitor.Command import Command
from apcIpmiMonitor.Formatter.ServerStatusFormatter import ServerStatusFormatter

cli = click.Group()

@cli.group()
def monitoring():
    pass

@monitoring.command()
@click.option("-f", "--config-path", required=True, help="Path to your config file.", type=click.Path(exists=True))
def server_status(config_path):
    config = Config(config_path)
    servers = config.get_servers()
    gateway = IpmiGateway(Command("ipmitool"))
    formatter = ServerStatusFormatter(gateway)

    click.echo(formatter.format_server_list_to_table(servers))

@monitoring.command()
@click.option("-f", "--config-path", required=True, help="Path to your config file.", type=click.Path(exists=True))
def run(config_path):
    config = Config(config_path)
    servers = config.get_servers()

    ipmi_gateway = IpmiGateway(Command("ipmitool"))
    apc_gateway = ApcGateway(Command("apcaccess"))

    formatter = ServerStatusFormatter(ipmi_gateway)

    if apc_gateway.is_fully_charged():
        click.echo("Battery is plugged in & fully charged. No action is required...")
        exit(0)

    field = config.to_dict()["apc_shutdown_threshold"]["field"]
    threshold = config.to_dict()["apc_shutdown_threshold"]["value"]

    if apc_gateway.is_online():
        click.echo(f"Batter is back online, status upgraded to 'degraded' status. Waiting for batter to reach 100%.")
        exit(0)

    if float(apc_gateway.get_field(field).split(" ")[0]) > float(threshold):
        click.echo(f"APC '{field}' is above the '{threshold}' threshold. No action needed for this iteration.")
        exit(0)

    click.echo(f"APC had dropped bellow the '{threshold}' threshold for '{field}'. Shutting down all servers...")

    for server in servers:
        if ipmi_gateway.get_status(server) == "Online":
            ipmi_gateway.trigger_soft_shutdown(server)

    click.echo("All servers have been issued a shutdown command...")

    click.echo(formatter.format_server_list_to_table(servers))


if __name__ == "__main__":
    cli()
