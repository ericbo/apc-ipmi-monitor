import yaml

from ApcSession import ApcSession
from IpmiSession import IpmiSession
from ServerSessions import ServerSessions


def load_from_config():
    with open("../config.yaml", "r") as file:
        data = yaml.safe_load(file)

    return data

def main():
    sessions = []
    configs = load_from_config()
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
    main()