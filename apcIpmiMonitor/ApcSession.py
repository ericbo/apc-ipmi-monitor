import os
from apcIpmiMonitor.Command import Command


class ApcSession(object):
    def __init__(self, binary: str):
        self.__command = Command(binary, [])

    def info(self):
        #return self.__command.run([])
        return self.get_field("STATUS")

    def is_fully_charged(self):
        charge = self.get_field("BCHARGE").split(" ")[0]
        status = self.get_field("STATUS")

        return charge == "100.0" and status == "ONLINE"

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