# Author: Hoani
#
# Provides a fake socket which can be used to test the application without a connection

from datetime import datetime
import random

class SocketFake():
  def __init__(self, mac_addr, port):
    self.server = (mac_addr, port)
    self.connected = False
    self.last_timestamp = datetime.now().timestamp()

  def connect(self):
    print("Attempting to connect to", self.server)
    print("Connected to", self.server)
    self.connected = True
  
  def recv(self, bytes=1024):
    now = datetime.now().timestamp()
    if (now - self.last_timestamp >= 0.100):
      self.last_timestamp += 0.100
      payload = ('' + \
        'accel {:0.3f} {:0.3f} {:0.3f}\n' +\
        'gyros {:0.3f} {:0.3f} {:0.3f}\n' +\
        'magne {:0.3f} {:0.3f} {:0.3f}\n' +\
        '').format(
            8.8 + 2.0*random.random(), -0.5 + 2.0*random.random(), -0.3 + random.random(),
            0.2 + 0.4*random.random(), -0.6 + 1.0*random.random(), -0.5 + 0.8*random.random(),
            25.0 + 6.0*random.random(), -10.0 + 5.0*random.random(), -30.0 + 4.0*random.random()
        ).encode('utf-8')
      return payload
    else:
      raise OSError("No Data")

  def send(self, packet):
    print("sent", packet)

  def close(self):
    pass

