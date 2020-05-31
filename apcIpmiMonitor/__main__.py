import importlib
import sys

import click

# Add apcIpmiMpnitor to dev workspace
if not importlib.util.find_spec("apcIpmiMonitor"):
    sys.path.insert(0, ".")

from apcIpmiMonitor.ApcSession import ApcSession
from apcIpmiMonitor.IpmiSession import IpmiSession
from apcIpmiMonitor.Config import Config
from apcIpmiMonitor.Repository.IpmiGateway import IpmiGateway
from apcIpmiMonitor.Command import Command
from apcIpmiMonitor.Formatter.ServerStatusFormatter import ServerStatusFormatter
from apcIpmiMonitor.ServerSessions import ServerSessions

cli = click.Group()

@cli.group()
def monitoring():
    pass

@monitoring.command()
@click.option("-f", "--config", required=True, help="Path to your config file.", type=click.Path(exists=True))
def server_status(config):
    config = Config(config)
    servers = config.get_servers()
    gateway = IpmiGateway(Command("ipmitool", []))
    formatter = ServerStatusFormatter(gateway)

    click.echo(formatter.format_server_list_to_table(servers))

@monitoring.command()
@click.option("-f", "--config", help="Path to your config file.", type=click.Path(exists=True))
def run(config):
    sessions = []
    configs = Config(config).to_dict()
    apc = ApcSession(configs.get("apcaccess_binary"))

    if apc.is_fully_charged():
        print("APC is charged and using wall power, closing...")
        exit(0)

    field = configs["apc_shutdown_threshold"]["field"]
    threshold = configs["apc_shutdown_threshold"]["value"]

    if not apc.is_on_battery():
        print("APC is back online. No action needed for this iteration.")
        exit(0)

    if float(apc.get_field(field).split(" ")[0]) > float(threshold):
        print(f"APC '{field}' is above the '{threshold}' threshold. No action needed for this iteration.")
        exit(0)

    print(f"APC had dropped bellow the '{threshold}' threshold for '{field}'. Shutting down all servers...")

    for server in configs.get("servers", []):
        conf = configs.get("servers", [])[server]
        session = IpmiSession(
            configs.get("ipmitool_binary"),
            conf.get("hostname"),
            conf.get("username"),
            conf.get("password")
        )
        try:
            session.power_status()
        except Exception as e:
            print(f"Failed to connect to server '{server}'. Will skip for this iteration.\n{e}")
            continue

        sessions.append(session)

    server_sessions = ServerSessions(sessions)

    server_sessions.shutdown_all()

    print("All servers have been shutdown...")

if __name__ == "__main__":
    cli()