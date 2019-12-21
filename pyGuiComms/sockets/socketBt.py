# Author: Hoani
#
# Provides a bluetooth client socket which can be accessed for communications.
try:
  import bluetooth

  class SocketBt(bluetooth.BluetoothSocket):
    def __init__(self, mac_addr, port):
      self.server = (mac_addr, port)
      self.connected = False
      super().__init__(bluetooth.RFCOMM)

    def connect(self):
      print("Attempting to connect to", self.server)
      self.setblocking(True)
      super().connect(self.server)
      self.setblocking(False) # Non blocking
      print("Connected to", self.server)
      self.connected = True


  if __name__ == '__main__':

    serverMACAddress = '38:D2:69:E1:11:CB'
    port = 3
    s = BtClient(serverMACAddress, port)

    while True:
      try:
        s.connect()
        break
      except:
        pass
    while True:
      text = input()
      s.setblocking(True)
      if text == "quit":
        break
      s.send(text)
      data = s.recv(1024)
      if data:
        print("received: ", data)
    s.close()
except:
  print("No bluetooth found")