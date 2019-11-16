from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets, QtGui
import sys, os
import numpy as np
try:
  import qdarkstyle
except:
  pass

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.show()
    self.command_queue = None
    self.upkeep_timer = []
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

  def update_plot_vec3(self, item, vec3):
    if item == None:
      return
    else:
      item.update_data(vec3)

  def set_command_queue(self, queue):
    self.command_queue = queue

  def command_queue_place(self, item):
    self.command_queue.put(item)



