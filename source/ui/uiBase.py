from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import sys, os
import datetime
import numpy as np
try:
  import qdarkstyle
except:
  pass

def load_from_file(filepath):
  ui_file = QFile(filepath)
  ui_file.open(QFile.ReadOnly)
  loader = QUiLoader()
  loader.registerCustomWidget(MainWindow)
  window = loader.load(ui_file)
  ui_file.close()
  return window



class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.show()
    self.command_queue = None
    self.upkeep_timer = []
    self.ui_objs = []
    try:
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    except:
        pass

  def add_upkeep(self, period_ms, callback):
    timer = QtCore.QTimer(self)
    self.upkeep_timer.append(timer)
    timer.start(period_ms)
    timer.timeout.connect(callback)

  def update_text_field(self, item, value, pattern="{:.3f}"):
    if item == None:
      return
    else:
      item.setText(pattern.format(value))

  def update_plot_vec3(self, item, t, vec3):
    if item == None:
      return
    else:
      item.update_data(t, vec3)

  def set_command_queue(self, queue):
    self.command_queue = queue

  def command_queue_place(self, item):
    self.command_queue.put(item)

  def load_ui_elements(self, ui_element_list, comms, log_entries):
    if log_entries != None:
      log_entries.add('timestamp', self._get_timestamp)

    for idx, ui_element in enumerate(ui_element_list):
      ui = ui_element.Ui(self)
      ui.set_subscriptions(comms.subscribe)
      if log_entries != None:
        ui.add_log_entries(log_entries)
      self.ui_objs.append(ui)

  def _get_timestamp(self):
    return datetime.datetime.now().timestamp()



