# Author: Hoani
#
# Client remote logging class, dumps all received packets into a CSV log

import sys, os, datetime

class RemoteLogClient():
  def __init__(self, client = None, data_map = None):
    self.client = client
    self.current_file = None
    self.client_connecting = False
    self.remainder = ""
    self.data_map = data_map

  def upkeep(self):
    if self.client == None:
      return
    
    if 'rlog/active' in self.data_map:
      logging_active = self.data_map['rlog/active']
    else:
      logging_active = False

    if self.current_file == None and logging_active == True:
      filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-rlog.csv")
      self.current_file = open(filename, 'w')

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

    if self.current_file != None and logging_active == False:
      self.current_file = self.current_file.close()


  def _process_packet(self, data):
    data = self.remainder + data.decode('utf-8')
    lines = data.split('\n')
    self.remainder = lines[-1]
    loggable = "\n".join(lines[:-1])
    
    if self.current_file == None:
      print(loggable)
    else:
      self.current_file.write(loggable + '\n')

