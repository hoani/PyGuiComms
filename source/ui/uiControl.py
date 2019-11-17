from PySide2 import QtWidgets
import sys, os

class Ui():
  def __init__(self, main_window):
    self.main_window = main_window

    self.manual_upkeep = None
    self.command_queue = None

    self.main_window.add_upkeep(50, self._manual_upkeep)

    button_disable   = self.main_window.findChild(QtWidgets.QPushButton, 'controlDisable')
    button_auto      = self.main_window.findChild(QtWidgets.QPushButton, 'controlAuto')
    button_manual_fw = self.main_window.findChild(QtWidgets.QPushButton, 'controlManualFW')
    button_manual_bw = self.main_window.findChild(QtWidgets.QPushButton, 'controlManualBW')
    button_manual_lt = self.main_window.findChild(QtWidgets.QPushButton, 'controlManualLT')
    button_manual_rt = self.main_window.findChild(QtWidgets.QPushButton, 'controlManualRT')

    if button_disable != None:
      button_disable.clicked.connect(self._control_disable)

    if button_auto != None:
      button_auto.clicked.connect(self._control_auto)

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

    self.slider_manual_speed = self.main_window.findChild(QtWidgets.QSlider, 'manualSpeed')
    if self.slider_manual_speed != None:
      self.slider_manual_speed.sliderReleased.connect(self._manual_speed) 
    self.manual_speed = 0.5

  def set_subscriptions(self, subscribe):
    return

  def _manual_upkeep(self):
    if self.manual_upkeep != None:
      self.manual_upkeep()

  def _control_disable(self):
    self.main_window.command_queue_place(('disable'))

  def _control_auto(self):
    self.main_window.command_queue_place(('auto'))

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
    self.main_window.command_queue_place(('manual', dir, self.manual_speed))

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
