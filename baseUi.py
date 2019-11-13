from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets
import extraConsole
import sys
import vect
try:
    import qdarkstyle
except:
    pass

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.client = None
    self.show()
    try:
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    except:
        pass

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
          print(data.decode('utf-8'))
          self._process_packet(data)
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

    self.accelerometer = vect.Vec3(
      self.findChild(QtWidgets.QLineEdit, 'acc_x'),
      self.findChild(QtWidgets.QLineEdit, 'acc_y'),
      self.findChild(QtWidgets.QLineEdit, 'acc_z')
    )

    self.gyroscope = vect.Vec3(
      self.findChild(QtWidgets.QLineEdit, 'gyro_x'),
      self.findChild(QtWidgets.QLineEdit, 'gyro_y'),
      self.findChild(QtWidgets.QLineEdit, 'gyro_z')
    )

    self.magnetometer = vect.Vec3(
      self.findChild(QtWidgets.QLineEdit, 'mag_x'),
      self.findChild(QtWidgets.QLineEdit, 'mag_y'),
      self.findChild(QtWidgets.QLineEdit, 'mag_z')
    )


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

  def _process_packet(self, data):
    data = data.decode('utf-8')
    for line in data.split('\n'):
      items = line.split(' ')
      if items[0] == "accel":
        if len(items) == 4:
          self.accelerometer.x.setText("{:.2f}".format(float(items[1])))
          self.accelerometer.y.setText("{:.2f}".format(float(items[2])))
          self.accelerometer.z.setText("{:.2f}".format(float(items[3])))

      if items[0] == "gyros":
        if len(items) == 4:
          self.gyroscope.x.setText("{:.2f}".format(float(items[1])))
          self.gyroscope.y.setText("{:.2f}".format(float(items[2])))
          self.gyroscope.z.setText("{:.2f}".format(float(items[3])))

      if items[0] == "magne":
        if len(items) == 4:
          self.magnetometer.x.setText("{:.2f}".format(float(items[1])))
          self.magnetometer.y.setText("{:.2f}".format(float(items[2])))
          self.magnetometer.z.setText("{:.2f}".format(float(items[3])))