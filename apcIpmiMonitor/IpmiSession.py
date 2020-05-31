from apcIpmiMonitor.Command import Command

class IpmiSession(object):
    def __init__(self, binary: str, ip: str, username: str, password: str):
        self.__command = Command(binary, ["-H", ip, "-U", username, "-P", password])
        self.__command.secret(password)

    def power_status(self):
        return self.__command.run(["chassis", "power", "status"])

    def is_powered_on(self):
        status = self.power_status().split(" ")[-1]

        return status == "on"

    def is_powered_off(self):
        status = self.power_status().split(" ")[-1]

        return status == "off"

    def power_off(self):
        return self.__command.run(["chassis", "power", "soft"])

    def power_on(self):
        return self.__command.run(["chassis", "power", "on"])
