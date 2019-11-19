# Author: Hoani
#
# Client comms object for sending intercepting and delivering packets to Application 
# subscribers.
#
# Data flow:
#     Socket -> CommsClient -> Subscribers
# Eventually a translation object will subscribe to comms client and will take application subscribers.

import sys, os
from source.utilities import vect
import queue

class CommsClient():
  def __init__(self, client = None, my_queue = queue.Queue()):
    self.client = client
    self.client_connecting = False
    self.subscribers = dict()
    self.command_queue = my_queue

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
          print(data.decode('utf-8'))
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
          command = self.command_queue.get_nowait()
          if command == " " or command == (""):
            raise Exception("WTF?!")

          if command == None or command == False:
            break
          if isinstance(command, list) == False:
            if isinstance(command, str):
              command = [command]
            else:
              command = list(command)

          for idx, item in enumerate(command):
            if isinstance(item, str):
              continue
            elif isinstance(item, float):
              command[idx] = "{:0.2f}".format(item)
            else:
              command[idx] = str(item)
          # Opportunity for improvement - verification of commands
          payload = " ".join(command) + "\n"
          payload = payload.encode('utf-8')
          self.client.send(payload)
          
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

  def _publish(self, item, payload):
    if item in self.subscribers.keys():
      for callback in self.subscribers[item]:
        callback(payload)

  def _process_packet(self, data):
    data = data.decode('utf-8')
    for line in data.split('\n'):
      items = line.split(' ')

      if items[0] == "accel" or items[0] == "gyros" or items[0] == "magne":
        if len(items) == 4:
          accel_data = vect.Vec3(
            float(items[1]),
            float(items[2]),
            float(items[3])
          )
          self._publish(items[0], accel_data)