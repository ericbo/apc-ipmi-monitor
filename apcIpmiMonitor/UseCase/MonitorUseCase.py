from apcIpmiMonitor.Infrastructure import ApcGateway
from apcIpmiMonitor.Infrastructure.IpmiGateway import IpmiGateway


class MonitorUseCase(object):
    def __init__(self, apc_gateway: ApcGateway, ipmi_gateway: IpmiGateway):
        self.__apc_gateway = apc_gateway
        self.__ipmi_gateway = ipmi_gateway

    def exec(self, servers: list):
        pass