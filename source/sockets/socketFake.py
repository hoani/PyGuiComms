

class SocketFake():
  def __init__(self, mac_addr, port):
    self.server = (mac_addr, port)
    self.connected = False

  def connect(self):
    print("Attempting to connect to", self.server)
    print("Connected to", self.server)
    self.connected = True
  
  def recv(self, bytes=1024):
    raise OSError("No Data")

  def send(self, packet):
    print("sent", packet)

  def close(self):
    pass

