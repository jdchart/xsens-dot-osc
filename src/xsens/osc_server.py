from pythonosc import udp_client

class OSCSender:
    def __init__(self, **kwargs) -> None:
        self.ip = kwargs.get("ip", "127.0.0.1")
        self.port = kwargs.get("port", 12345)
        self.client = None

    def start_server(self):
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

    def send(self, address, message):
        self.client.send_message(address, message)