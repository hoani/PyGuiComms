# Author: Hoani
#
# Provides a fake socket which can be used to test the application without a connection

from datetime import datetime
import random
from leap import codec, packet

class SocketFake():
  def __init__(self, mac_addr, port):
    self.server = (mac_addr, port)
    self.connected = False
    self.last_timestamp = datetime.now().timestamp()
    self.codec = leap.Codec('config/protocol.json')

  def connect(self):
    print("Attempting to connect to", self.server)
    print("Connected to", self.server)
    self.connected = True
  
  def recv(self, bytes=1024):
    now = datetime.now().timestamp()
    if (now - self.last_timestamp >= 0.100):
      self.last_timestamp += 0.100

      p = leap.Packet("pub", 'imu', tuple([
          8.8 + 2.0*random.random(), -0.5 + 2.0*random.random(), -0.3 + random.random(),
          0.2 + 0.4*random.random(), -0.6 + 1.0*random.random(), -0.5 + 0.8*random.random(),
          25.0 + 6.0*random.random(), -10.0 + 5.0*random.random(), -30.0 + 4.0*random.random()
        ])
      )
      

      encoded = self.codec.encode(p)

      return encoded
    else:
      raise OSError("No Data")

  def send(self, packet):
    print("sent", packet)

  def close(self):
    pass

