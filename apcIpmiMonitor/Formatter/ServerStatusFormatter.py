from tabulate import tabulate

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ServerStatusFormatter(object):
    def __init__(self, ipmi_gateway):
        self.__ipmi_gateway = ipmi_gateway

    def format_server_list_to_table(self, servers: list):
        statuses = [["Server Name", "User", "Hostname", "Status"]]

        for server in servers:
            status = self.__ipmi_gateway.get_status(server)

            statuses.append([
                server.name,
                server.username,
                server.hostname,
                self.__format_status(status)
            ])
        print(statuses)

        return tabulate(statuses, tablefmt="pretty")

    @staticmethod
    def __format_status(status: str):
        if status.endswith("on"):
            return ServerStatusFormatter.__color_text(status, "green")

        if status.endswith("off"):
            return ServerStatusFormatter.__color_text(status, "red")

        return ServerStatusFormatter.__color_text(status, "yellow")

    @staticmethod
    def __color_text( text: str, color: str):
        colors = {
            "red": "\u001b[31m",
            "green": "\u001b[32m",
            "yellow": "\u001b[38;5;166m",
            "blue": "\u001b[34m",
            "reset": "\u001b[0m",
        }

        return f"{colors.get(color, '')}{text}{colors.get('reset')}"