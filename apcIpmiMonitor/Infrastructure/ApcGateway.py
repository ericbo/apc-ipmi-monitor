import os

from apcIpmiMonitor.Command import Command


class ApcGateway(object):
    def __init__(self, command: Command):
        self.__command = command

    def is_fully_charged(self):
        charge = self.get_field("BCHARGE").split(" ")[0]

        return charge == "100.0" and self.is_online()

    def is_online(self):
        return self.get_field("STATUS") == "ONLINE"

    def is_on_battery(self):
        status = self.get_field("STATUS")
        return status == "ONBATT"

    def get_field(self, field: str):
        return self.get_info()[field]

    def get_info(self):
        info = {}
        output = self.__command.run([])

        all_fields = output.split(os.linesep)

        for field in all_fields:
            if ":" not in field:
                continue

            info.update(self.__get_key_value(field))

        return info

    def __get_key_value(self, line):
        key, value = line.split(":", 1)

        return {key.strip(): value.strip()}