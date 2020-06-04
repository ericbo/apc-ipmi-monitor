import yaml

from apcIpmiMonitor.Domain.Server import Server


class Config(object):
    def __init__(self, config_path: str):
        self.__config_path = config_path
        self.__config = self.__load_from_file(config_path)

    def get_servers(self):
        servers = []
        config_servers = self.__config.get("servers", [])

        for server in config_servers:
            servers.append(Server(server, **config_servers[server]))

        return servers

    def to_dict(self):
        return self.__config

    def get_path(self):
        return self.__config_path

    @staticmethod
    def __load_from_file(config):
        with open(config, "r") as file:
            data = yaml.safe_load(file)

        return data
