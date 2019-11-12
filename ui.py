import sys, io
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtWidgets
import extraConsole
import threading
import queue
import clientThread

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
        self.client_timer.stop()
        self.client.connect()
        self.client_timer.start(10) #Update rate in ms
      except:
        self.client_timer.singleShot(10, self._client_upkeep)
    else:
      try:
        data = self.client.recv(1024)
        if data != None:
          print(data)
        else:
          self.client.connected = False
          
      except OSError:
        pass
      except Exception as e:
        print(e)

  def init_signals(self):
    button_disable = self.findChild(QtWidgets.QPushButton, 'controlDisable')
    button_auto = self.findChild(QtWidgets.QPushButton, 'controlAuto')
    button_manual_fw = self.findChild(QtWidgets.QPushButton, 'controlManualFW')
    button_manual_bw = self.findChild(QtWidgets.QPushButton, 'controlManualBW')
    button_manual_lt = self.findChild(QtWidgets.QPushButton, 'controlManualLT')
    button_manual_rt = self.findChild(QtWidgets.QPushButton, 'controlManualRT')

    if button_disable != None:
      button_disable.clicked.connect(self._control_disable)
    if button_auto != None:
      button_auto.clicked.connect(self._control_auto)

    if button_manual_fw != None:
      button_manual_fw.clicked.connect(self._control_manual_forward) 
    if button_manual_bw != None:
      button_manual_bw.clicked.connect(self._control_manual_backward) 
    if button_manual_lt != None:
      button_manual_lt.clicked.connect(self._control_manual_left) 
    if button_manual_rt != None:
      button_manual_rt.clicked.connect(self._control_manual_right) 

    console = self.findChild(QtWidgets.QWidget, 'console')
    sys.stdout = extraConsole.extraConsole(console, QtWidgets.QTextEdit.insertPlainText)

    self.slider_manual_speed = self.findChild(QtWidgets.QSlider, 'manualSpeed')
    if self.slider_manual_speed != None:
      self.slider_manual_speed.sliderReleased.connect(self._manual_speed) 
    self.manual_speed = 0.5


  def _control_disable(self):
    self._client_send(b'disable')

  def _control_auto(self):
    self._client_send(b'auto')

  def _manual_speed(self):
    self.manual_speed = self.slider_manual_speed.value()/100.0

  def _control_manual_forward(self):
    self._control_manual_cmd("FW")
  
  def _control_manual_backward(self):
    self._control_manual_cmd("BW")
  
  def _control_manual_left(self):
    self._control_manual_cmd("LT")
  
  def _control_manual_right(self):
    self._control_manual_cmd("RT")

  def _control_manual_cmd(self, dir):
    self._client_send(
      b'manual ' +
      dir.encode('utf-8') +
      b' ' +
      "{:0.2f}".format(self.manual_speed).encode('utf-8') +
      b' '
      )

  def _client_send(self, data):
    if self.client == None:
      return
    else:
      self.client.send(data)



if __name__ == '__main__':
  echo = False
  serverMACAddress = '38:D2:69:E1:11:CB'
  port = 3
  if echo == True:
    import echoClient
    ClientSocket = echoClient.EchoClient
  else:
    import btClient
    ClientSocket = btClient.BtClient
    
  
  client_socket = ClientSocket(serverMACAddress, port)

  app = QApplication(sys.argv)
  #ui_file = QFile('BasicCommands.ui')
  ui_file = QFile('ManualControl.ui')
  ui_file.open(QFile.ReadOnly)

  loader = QUiLoader()
  loader.registerCustomWidget(MainWindow)
  window = loader.load(ui_file)
  window.init_signals()
  window.register_client(client_socket) 

  ui_file.close()


  sys.exit(app.exec_())



  

