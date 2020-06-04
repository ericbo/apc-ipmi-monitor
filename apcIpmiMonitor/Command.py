import subprocess

class Command(object):
    def __init__(self, binary: str):
        self.__base_command = [binary]
        self.__secret = None

    def secret(self, secret: str):
        self.__secret = secret

    def run(self, args: list):
        command = [*self.__base_command, *args]
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if len(response.stderr) > 0:
            raise ValueError(self.__decode_response(response.stderr))

        return self.__decode_response(response.stdout)

    def __decode_response(self, response: bin):
        encoding = "utf-8"

        if self.__secret:
            return response.decode(encoding).replace(self.__secret, "*****")

        return response.decode(encoding)
