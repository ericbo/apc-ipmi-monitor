from apcIpmiMonitor.Command import Command
from apcIpmiMonitor.Domain.Server import Server


class IpmiGateway(object):
    def __init__(self, command: Command):
        self.__command = command

    def get_status(self, server: Server):
        args = [*self.__create_credential_args(server), *["chassis", "power", "status"]]
        self.__command.secret(server.password)

        try:
            return self.__command.run(args).rstrip()
        except ValueError:
            return "Unknown (Connection Timeout)"

    def trigger_soft_shutdown(self, server: Server):
        args = [*self.__create_credential_args(server), *["chassis", "power", "soft"]]
        return self.__command.run(args)

    @staticmethod
    def __create_credential_args(server: Server):
        return [
            "-H", server.hostname,
            "-U", server.username,
            "-P", server.password
        ]
