from PySide2 import QtWidgets, QtGui
from source.ui import extraConsole
import sys, os

class Ui:
  def __init__(self, main_window):
    self.main_window = main_window

    self.console = self.main_window.findChild(QtWidgets.QWidget, 'console')
    if self.console != None:
      sys.stdout = extraConsole.extraConsole(self.console, QtWidgets.QTextEdit.insertPlainText)
      self.console.textChanged.connect(self._console_cursor)

  def set_subscriptions(self, subscribe):
    pass

  def add_log_entries(self, log_entries):
    pass

  def _console_cursor(self):
    self.console.moveCursor(QtGui.QTextCursor.End)
