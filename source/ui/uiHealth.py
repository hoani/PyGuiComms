# Author: Hoani
# 
# Contains UI logic for displaying and sending health related commands
# Health includes:
# - CPU usage
# - Battery Voltage
# - Link health


from PySide2 import QtWidgets
import sys, os
from source.utilities import vect
from source.ui import plotCanvas

class Ui():
  def __init__(self, main_window):
    self.main_window = main_window

    self.plot_layout = self.main_window.findChild(QtWidgets.QVBoxLayout, "plotCpuUsage")

    self.data_max = 50

    self.plot_cpu_usage = plotCanvas.PlotCanvas(0, title="Accel (%)")
    self.plot_layout.addWidget(self.plot_cpu_usage)

    self.label_cpu_usage = self.main_window.findChild(QtWidgets.QLineEdit, 'labelCpuUsage')
    self.label_battery_voltage = self.main_window.findChild(QtWidgets.QLineEdit, 'labelBatteryVoltage')

    self.data_cpu_usage = 0
    self.data_battery_voltage = 0

  def set_subscriptions(self, subscribe):
    subscribe('cpuse', self._data_update_cpu_usage)
    subscribe('battv', self._data_update_battery_voltage)

  def add_log_entries(self, log_entries):
    log_entries.add('cpu-usage', self._get_cpu_usage)
    log_entries.add('batt-voltage', self._get_battery_voltage)

  def _data_update_cpu_usage(self, data):
    self.main_window.update_plot_vec3(self.plot_cpu_usage, data)
    self.main_window.update_text_field(self.label_cpu_usage, data)
    self.data_cpu_usage = data

  def _data_update_battery_voltage(self, data):
    self.main_window.update_plot_vec3(self.plot_battery_voltage, data)
    self.main_window.update_text_field(self.label_battery_voltage, data)
    self.data_battery_voltage = data

  def _get_cpu_usage(self):
    return self.data_cpu_usage

  def _get_battery_voltage(self):
    return self.data_battery_voltage

