from PySide2 import QtWidgets
import sys, os
from source.utilities import vect
from source.ui import plotCanvas

class Ui():
  def __init__(self, main_window):
    self.main_window = main_window
    # self.main_window.add_ui(self)

    self.plot_layout = self.main_window.findChild(QtWidgets.QVBoxLayout, "plotLayout")

    self.data_max = 50

    self.plot_accel = plotCanvas.PlotCanvas(vect.Vec3(0,0,0), title="Accel (m/s^2)")
    self.plot_gyro = plotCanvas.PlotCanvas(vect.Vec3(0,0,0), title="Gyro (deg/s)")
    self.plot_mag = plotCanvas.PlotCanvas(vect.Vec3(0,0,0), title="Mag (mT)")
    self.plot_layout.addWidget(self.plot_accel)
    self.plot_layout.addWidget(self.plot_gyro)
    self.plot_layout.addWidget(self.plot_mag)

    self.accelerometer = vect.Vec3(
      self.main_window.findChild(QtWidgets.QLineEdit, 'acc_x'),
      self.main_window.findChild(QtWidgets.QLineEdit, 'acc_y'),
      self.main_window.findChild(QtWidgets.QLineEdit, 'acc_z')
    )

    self.gyroscope = vect.Vec3(
      self.main_window.findChild(QtWidgets.QLineEdit, 'gyro_x'),
      self.main_window.findChild(QtWidgets.QLineEdit, 'gyro_y'),
      self.main_window.findChild(QtWidgets.QLineEdit, 'gyro_z')
    )

    self.magnetometer = vect.Vec3(
      self.main_window.findChild(QtWidgets.QLineEdit, 'mag_x'),
      self.main_window.findChild(QtWidgets.QLineEdit, 'mag_y'),
      self.main_window.findChild(QtWidgets.QLineEdit, 'mag_z')
    )

  def set_subscriptions(self, subscribe):
    subscribe('accel', self._data_update_accelerometer)
    subscribe('gyros', self._data_update_gyroscope)
    subscribe('magne', self._data_update_magnetometer)

  def _data_update_accelerometer(self, data):
    self.main_window.update_text_field(self.accelerometer.x, data.x)
    self.main_window.update_text_field(self.accelerometer.y, data.y)
    self.main_window.update_text_field(self.accelerometer.z, data.z)
    self.main_window.update_plot_vec3(self.plot_accel, data)

  def _data_update_gyroscope(self, data):
    self.main_window.update_text_field(self.gyroscope.x, data.x)
    self.main_window.update_text_field(self.gyroscope.y, data.y)
    self.main_window.update_text_field(self.gyroscope.z, data.z)
    self.main_window.update_plot_vec3(self.plot_gyro, data)

  def _data_update_magnetometer(self, data):
    self.main_window.update_text_field(self.magnetometer.x, data.x)
    self.main_window.update_text_field(self.magnetometer.y, data.y)
    self.main_window.update_text_field(self.magnetometer.z, data.z)
    self.main_window.update_plot_vec3(self.plot_mag, data)
