import threading
import queue

class clientThread(threading.Thread):
  def __init__(self, client, tx_queue, rx_queue):
    threading.Thread.__init__(self)
    self.client = client
    self.close_request = threading.Event()
    self.tx_queue = tx_queue
    self.rx_queue = rx_queue

  def run(self):
    while not self.close_request.isSet():
      try:
        self.client.connect()
        break
      except:
        pass
    while not self.close_request.isSet():
      try:
        data = self.client.recv(1024)
        if data:
          self.rx_queue.put(data)
          print(data)
      except OSError:
        pass
      except Exception as e:
        print(e)
      try:
        data = self.tx_queue.get_nowait()
        self.client.send(data)
      except queue.Empty:
        pass
      except Exception as e:
        print(e)
        pass

    self.client.close()

  def join(self, timeout=None):
    self.close_request.set()
    super(clientThread, self).join(timeout)