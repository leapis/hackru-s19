import telnetlib

class Emulator:

    def __init__(self, port, debug=False):
        self.__connect(port, debug)
        self.__send_command("auth Mvyn7x27JDXUgbvW")

    def __connect(self, port, debug=False):
        if debug:
            print("Initiating connection to port {}...".format(port))

        self.conn = telnetlib.Telnet("localhost", port)
        self.conn.read_until(b"OK")

        if debug:
            print("Connection established.")

    def send_sms(self, number, message):
        """Send an SMS containing <message> from <number>"""
        self.__send_command("sms send {} {}".format(number, message))

    def call(self, number):
        """Simulate a call from <number>"""
        self.__send_command("gsm call {}".format(number))

    def accept_call(self, number):
        """Command the emulator to accept the incoming call from <number>"""
        self.__send_command("gsm accept {}".format(number))

    def cancel_call(self, number):
        """Cancel a phone call previously sent from <number>"""
        self.__send_command("gsm cancel {}".format(number))

    def __send_command(self, command):
        real_command = bytes("{}\n".format(command), "ascii")
        self.conn.write(real_command)
