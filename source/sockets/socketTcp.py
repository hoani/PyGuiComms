
import socket

class SocketTcp(socket.socket):
  def __init__(self, ip_addr, port):
    self.server = (ip_addr, port)
    self.connected = False
    super().__init__(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self):
    print("Attempting to connect to", self.server)
    self.setblocking(True)
    super().connect(self.server)
    self.setblocking(False) # Non blocking
    print("Connected to", self.server)
    self.connected = True