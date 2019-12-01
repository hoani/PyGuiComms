# Author: Hoani
#
# Client comms object for sending intercepting and delivering packets to Application 
# subscribers.
#
# Data flow:
#     Socket -> CommsClient -> Subscribers
# Eventually a translation object will subscribe to comms client and will take application subscribers.

import sys, os
from pyGuiComms.utilities import vect
import queue
from external.RoBus.RoBus import codec, packet

class CommsClient():
  def __init__(self, protocol_file_path, client = None, my_queue = queue.Queue()):
    self.client = client
    self.client_connecting = False
    self.subscribers = dict()
    self.command_queue = my_queue
    self.remainder = b""
    self.codec = codec.Codec(protocol_file_path)

  def upkeep(self):
    if self.client == None:
      return

    if self.client.connected == False:
      if self.client_connecting == False:
        self.client_connecting = True
        try:
          self.client.connect()
        except:
          pass
        self.client_connecting = False
    else:
      try:
        data = self.client.recv(1024)
        if data != None:
          self._process_packet(data)
        else:
          self.client.connected = False
        
      except OSError:
        pass
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type,',', fname,', ln', exc_tb.tb_lineno)
        print(e)

      while True:
        try:
          path, payload = self.command_queue.get_nowait()

          p = packet.Packet("set", path, payload)
          encoded = self.codec.encode(p)
          if encoded != '':
            self.client.send(encoded)
          
        except queue.Empty:
          break
        except Exception as e:
          exc_type, exc_obj, exc_tb = sys.exc_info()
          fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
          print(exc_type,',', fname,', ln', exc_tb.tb_lineno)
          print(e)

  def _client_send(self, data):
    if self.client == None:
      return
    else:
      self.client.send(data)

  def subscribe(self, item, callback):
    if item in self.subscribers.keys():
      self.subscribers[item].append(callback)
    else:
      self.subscribers[item] = [callback]

  def _publish(self, unpacked):
    for subscription in self.subscribers.keys():
      data = []
      for item in unpacked.keys():
        if subscription in item:
          data.append(unpacked[item]["value"])

      if len(data) > 0:
        for callback in self.subscribers[subscription]:
          callback(data)

  def _process_packet(self, data):
    data = self.remainder + data
    
    (self.remainder, packets) = self.codec.decode(data)
    for p in packets:
      if p.category == "pub":
        unpacked = p.unpack(self.codec)
        self._publish(unpacked)
