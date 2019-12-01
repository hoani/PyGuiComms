from PySide2 import QtWidgets
import sys, os
from pyGuiComms.utilities import vect
from pyGuiComms.ui import plotCanvas
import datetime

class Ui():
  def __init__(self, main_window):
    self.t_start = datetime.datetime.now().timestamp()
    self.main_window = main_window

    self.plot_layout = self.main_window.findChild(QtWidgets.QVBoxLayout, "plotLayout")

    self.data_max = 50

    self.plot_accel = plotCanvas.XyzPlotCanvas(title="Accel (m/s^2)")
    self.plot_gyro = plotCanvas.XyzPlotCanvas(title="Gyro (deg/s)")
    self.plot_mag = plotCanvas.XyzPlotCanvas(title="Mag (mT)")
    self.plot_layout.addWidget(self.plot_accel)
    self.plot_layout.addWidget(self.plot_gyro)
    self.plot_layout.addWidget(self.plot_mag)

    self.accelerometer_data = vect.Vec3(0,0,0)
    self.gyroscope_data = vect.Vec3(0,0,0)
    self.magnetometer_data = vect.Vec3(0,0,0)

  def set_subscriptions(self, subscribe):
    subscribe('imu/accel/', self._data_update_accelerometer)
    subscribe('imu/gyros/', self._data_update_gyroscope)
    subscribe('imu/magne/', self._data_update_magnetometer)

  def add_log_entries(self, log_entries):
    log_entries.add('imu-accel-x', self._get_accelerometer_x)
    log_entries.add('imu-accel-y', self._get_accelerometer_y)
    log_entries.add('imu-accel-z', self._get_accelerometer_z)
    log_entries.add('imu-gyro-x', self._get_gyroscope_x)
    log_entries.add('imu-gyro-y', self._get_gyroscope_y)
    log_entries.add('imu-gyro-z', self._get_gyroscope_z)
    log_entries.add('imu-mag-x', self._get_magnetometer_x)
    log_entries.add('imu-mag-y', self._get_magnetometer_y)
    log_entries.add('imu-mag-z', self._get_magnetometer_z)

  def _data_update_accelerometer(self, data):
    t = datetime.datetime.now().timestamp() - self.t_start
    data = vect.Vec3(data)
    self.main_window.update_plot_vec3(self.plot_accel, t, data)
    self.accelerometer_data = data

  def _data_update_gyroscope(self, data):
    t = datetime.datetime.now().timestamp() - self.t_start
    data = vect.Vec3(data)
    self.main_window.update_plot_vec3(self.plot_gyro, t, data)
    self.gyroscope_data = data

  def _data_update_magnetometer(self, data):
    t = datetime.datetime.now().timestamp() - self.t_start
    data = vect.Vec3(data)
    self.main_window.update_plot_vec3(self.plot_mag, t, data)
    self.magnetometer_data = data

  def _get_accelerometer_x(self):
    return self.accelerometer_data.x

  def _get_accelerometer_y(self):
    return self.accelerometer_data.y

  def _get_accelerometer_z(self):
    return self.accelerometer_data.z

  def _get_gyroscope_x(self):
    return self.gyroscope_data.x

  def _get_gyroscope_y(self):
    return self.gyroscope_data.y

  def _get_gyroscope_z(self):
    return self.gyroscope_data.z

  def _get_magnetometer_x(self):
    return self.magnetometer_data.x

  def _get_magnetometer_y(self):
    return self.magnetometer_data.y

  def _get_magnetometer_z(self):
    return self.magnetometer_data.z

