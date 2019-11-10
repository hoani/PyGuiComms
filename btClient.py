"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""
import bluetooth

class btClient(bluetooth.BluetoothSocket):
  def __init__(self, mac_addr, port):
    self.server = (mac_addr, port)
    self.connected = False
    super().__init__(bluetooth.RFCOMM)

  def connect(self):
    print("Attempting to connect to", self.server)
    super().connect(self.server)
    super().setblocking(False) # Non blocking
    print("Connected to", self.server)
    self.connected = True


if __name__ == '__main__':

  serverMACAddress = '38:D2:69:E1:11:CB'
  port = 3
  s = btClient(serverMACAddress, port)

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