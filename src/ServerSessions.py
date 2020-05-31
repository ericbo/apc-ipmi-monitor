class ServerSessions(object):
    def __init__(self, ipmi_sessions: list):
        self.__ipmi_sessions = ipmi_sessions

    def shutdown_all(self):
        for session in self.__ipmi_sessions:
            if session.is_powered_on():
                try:
                    session.power_off()
                except:
                    print("Failed to shutdown server as server...")

    def power_on_all(self):
        for session in self.__ipmi_sessions:
            if session.is_powered_off():
                session.power_on()
