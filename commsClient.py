import sys, os
import vect

class CommsClient():
  def __init__(self, client = None):
    self.client = client
    self.client_connecting = False
    self.subscribers = dict()

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