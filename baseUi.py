from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets
import extraConsole
import sys
import vect
import math
import numpy as np
try:
  import qdarkstyle
except:
  pass
import plotCanvas


class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.client = None
    self.client_connecting = False
    self.show()
    self.upkeep_timer = []
    self.manual_upkeep = None
    self.add_upkeep(100, self._upkeep)
    self.add_upkeep(50, self._manual_upkeep)
    self.add_upkeep(10, self._client_upkeep)
    registration_timer = QtCore.QTimer(self)
    registration_timer.singleShot(1, self._register_widgets)
    try:
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    except:
        pass

  def add_upkeep(self, period_ms, callback):
    timer = QtCore.QTimer(self)
    self.upkeep_timer.append(timer)
    timer.start(period_ms)
    timer.timeout.connect(callback)

  def register_client(self, client):
    self.client = client

  def _upkeep(self):
    pass

  def _manual_upkeep(self):
    if self.manual_upkeep != None:
      self.manual_upkeep()

  def _client_upkeep(self):
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
        print(e)

  def _register_widgets(self):
    button_disable = self.findChild(QtWidgets.QPushButton, 'controlDisable')
    button_auto = self.findChild(QtWidgets.QPushButton, 'controlAuto')
    button_manual_fw = self.findChild(QtWidgets.QPushButton, 'controlManualFW')
    button_manual_bw = self.findChild(QtWidgets.QPushButton, 'controlManualBW')
    button_manual_lt = self.findChild(QtWidgets.QPushButton, 'controlManualLT')
    button_manual_rt = self.findChild(QtWidgets.QPushButton, 'controlManualRT')

    self.canvas_accel = self.findChild(QtWidgets.QGraphicsView, 'canvasAccel')
    self.canvas_gyro = self.findChild(QtWidgets.QGraphicsView, 'canvasGyro')
    self.canvas_mag = self.findChild(QtWidgets.QGraphicsView, 'canvasMag')

    self.plot_layout = self.findChild(QtWidgets.QVBoxLayout, "plotLayout")

    self.data_max = 50
    self.accel_index = 0
    self.accel_data = vect.Vec3(
      np.zeros(self.data_max),
      np.zeros(self.data_max),
      np.zeros(self.data_max)
      )
    self.gyro_index = 0
    self.gyro_data = vect.Vec3(
      np.zeros(self.data_max),
      np.zeros(self.data_max),
      np.zeros(self.data_max)
      )
    self.mag_index = 0
    self.mag_data = vect.Vec3(
      np.zeros(self.data_max),
      np.zeros(self.data_max),
      np.zeros(self.data_max)
      )

    self.plot_accel = plotCanvas.PlotCanvas(self.accel_data, title="Accel (m/s^2)")
    self.plot_gyro = plotCanvas.PlotCanvas(self.gyro_data, title="deg/s")
    self.plot_mag = plotCanvas.PlotCanvas(self.mag_data, title="Tesla")
    self.plot_layout.addWidget(self.plot_accel)
    self.plot_layout.addWidget(self.plot_gyro)
    self.plot_layout.addWidget(self.plot_mag)

    if button_disable != None:
      button_disable.clicked.connect(self._control_disable)
    if button_auto != None:
      button_auto.clicked.connect(self._control_auto)

    #can try connecting to pressed and released
    if button_manual_fw != None:
      button_manual_fw.pressed.connect(self._control_manual_forward_pressed)
      button_manual_fw.released.connect(self._control_manual_release)
    if button_manual_bw != None:
      button_manual_bw.pressed.connect(self._control_manual_backward_pressed)
      button_manual_bw.released.connect(self._control_manual_release)
    if button_manual_lt != None:
      button_manual_lt.pressed.connect(self._control_manual_left_pressed)
      button_manual_lt.released.connect(self._control_manual_release) 
    if button_manual_rt != None:
      button_manual_rt.pressed.connect(self._control_manual_right_pressed)
      button_manual_rt.released.connect(self._control_manual_release)

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
      b'\n'
      )

  def _control_manual_forward_pressed(self):
    self.manual_upkeep = self._control_manual_forward
  
  def _control_manual_backward_pressed(self):
    self.manual_upkeep = self._control_manual_backward
  
  def _control_manual_left_pressed(self):
    self.manual_upkeep = self._control_manual_left
  
  def _control_manual_right_pressed(self):
    self.manual_upkeep = self._control_manual_right

  

  def _control_manual_release(self):
    self.manual_upkeep = None
    self._control_disable()

  def _client_send(self, data):
    if self.client == None:
      return
    else:
      self.client.send(data)

  def _update_data(self, arr, value, index):
    if index == self.data_max:
      arr = np.roll(arr, 1)
      arr[self.data_max - 1] = value
    else:
      arr[index] = value


  def _process_packet(self, data):
    data = data.decode('utf-8')
    for line in data.split('\n'):
      items = line.split(' ')
      if items[0] == "accel":
        if len(items) == 4:
          self.accelerometer.x.setText("{:.2f}".format(float(items[1])))
          self.accelerometer.y.setText("{:.2f}".format(float(items[2])))
          self.accelerometer.z.setText("{:.2f}".format(float(items[3])))

          # self._update_data(self.accel_data.x, float(items[1]), self.accel_index)
          # self._update_data(self.accel_data.y, float(items[2]), self.accel_index)
          # self._update_data(self.accel_data.z, float(items[3]), self.accel_index)

          # if self.accel_index != self.data_max:
          #    self.accel_index += 1

          # self.plot_accel.plot(self.accel_data)
          self.plot_accel.update_data(vect.Vec3(float(items[1]), float(items[2]), float(items[3])))

      if items[0] == "gyros":
        if len(items) == 4:
          self.gyroscope.x.setText("{:.2f}".format(float(items[1])))
          self.gyroscope.y.setText("{:.2f}".format(float(items[2])))
          self.gyroscope.z.setText("{:.2f}".format(float(items[3])))

          # self._update_data(self.gyro_data.y, float(items[2]), self.gyro_index)
          # self._update_data(self.gyro_data.x, float(items[1]), self.gyro_index)
          # self._update_data(self.gyro_data.z, float(items[3]), self.gyro_index)

          # if self.gyro_index != self.data_max:
          #    self.gyro_index += 1

          # self.plot_gyro.plot(self.gyro_data)
          self.plot_gyro.update_data(vect.Vec3(float(items[1]), float(items[2]), float(items[3])))

      if items[0] == "magne":
        if len(items) == 4:
          self.magnetometer.x.setText("{:.2f}".format(float(items[1])))
          self.magnetometer.y.setText("{:.2f}".format(float(items[2])))
          self.magnetometer.z.setText("{:.2f}".format(float(items[3])))

          # self._update_data(self.mag_data.x, float(items[1]), self.mag_index)
          # self._update_data(self.mag_data.y, float(items[2]), self.mag_index)
          # self._update_data(self.mag_data.z, float(items[3]), self.mag_index)

          # if self.mag_index != self.data_max:
          #    self.mag_index += 1

          # self.plot_mag.plot(self.mag_data)
          self.plot_mag.update_data(vect.Vec3(float(items[1]), float(items[2]), float(items[3])))