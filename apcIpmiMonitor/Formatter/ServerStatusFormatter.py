from tabulate import tabulate


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
