import sys, io
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtWidgets
import btClient
import extraConsole
import threading
import queue
import clientThread

def control_disable():
  tx_queue.put(b'disable')

def control_auto():
  tx_queue.put(b'auto')

def console_update(text):
  console.insertPlainText(text)

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.client = None
    self.show()

  def register_client(self, client):
    if self.client == None:
      self.client_timer = QtCore.QTimer(self)
      self.client_timer.timeout.connect(self._client_upkeep)
      self.client_timer.singleShot(10, self._client_upkeep) #Update rate in ms

    self.client = client

  def _client_upkeep(self):
    if self.client.connected == False:
      try:
        self.client.connect()
        self.client_timer.start(10) #Update rate in ms
      except:
        self.client_timer.singleShot(10, self._client_upkeep)
    else:
      try:
        data = self.client.recv(1024)
        if data:
          print(data)
      except OSError:
        pass
      except Exception as e:
        print(e)

  def init_signals(self):
    button_disable = self.findChild(QtWidgets.QPushButton, 'controlDisable')
    button_auto = self.findChild(QtWidgets.QPushButton, 'controlAuto')
    t = QtWidgets.QPushButton
    if button_disable != None:
      button_disable.clicked.connect(self._control_disable)  
    if button_auto != None:
      button_auto.clicked.connect(self._control_auto) 
    console = self.findChild(QtWidgets.QWidget, 'console')
    sys.stdout = extraConsole.extraConsole(console, QtWidgets.QTextEdit.insertPlainText)


  def _control_disable(self):
    print("disable")
    self._client_send(b'disable')

  def _control_auto(self):
    self._client_send(b'auto')

  def _client_send(self, data):
    if self.client == None:
      return
    else:
      self.client.send(data)



if __name__ == '__main__':

  serverMACAddress = '38:D2:69:E1:11:CB'
  port = 3
  bt_socket = btClient.btClient(serverMACAddress, port)

  app = QApplication(sys.argv)
  ui_file = QFile('BasicCommands.ui')
  ui_file.open(QFile.ReadOnly)

  loader = QUiLoader()
  loader.registerCustomWidget(MainWindow)
  window = loader.load(ui_file)
  window.init_signals()
  window.register_client(bt_socket) 

  ui_file.close()


  sys.exit(app.exec_())



  

