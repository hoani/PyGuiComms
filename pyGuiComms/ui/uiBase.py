from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from pyGuiComms.utilities import vect
from pyGuiComms.ui import plotCanvas
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

class ValueCallback:
  def __init__(self, value):
    self._value = value

  def callback(self):
    return self._value


class ValueMapCallback:
  def __init__(self, value_map, key, default):
    self._value_map = value_map
    self._key = key
    self._default = default

  def callback(self):
    if self._key in self._value_map:
      return self._value_map[self._key]
    else:
      return self._default


class WidgetSubscriptionCallback:
  def __init__(self, callback, widget, config):
    self._callback = callback
    self._widget = widget
    self._config = config

  def callback(self, values):
    self._callback(self._widget, values, self._config)


class SetCallback:
  def __init__(self, queue_callback, path, payload_callbacks):
    self._callback = queue_callback
    self._path = path
    self._payload_callbacks = payload_callbacks

  def callback(self):
    payload = []
    for callback in self._payload_callbacks:
      payload.append(callback())

    self._callback(self._path, tuple(payload))

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.t_start = datetime.datetime.now().timestamp()
    self.show()
    self.command_queue = None
    self.upkeep_timer = []
    self.ui_objs = []
    self.callback_list = [] # This is used to avoid garbage collection
    self.uiValueMapping = {}
    try:
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    except:
        pass

    self.callback_map = {
      QtWidgets.QLineEdit: {
        "set": self.update_text_field 
      },
      QtWidgets.QVBoxLayout: {
        "setVec3": self.update_plot_vec3 
      }
    }

    self.widget_setup_map = {
      QtWidgets.QPushButton: {
        "pressed": self._setup_pressed,
        "released": self._setup_released 
      }
    }

    self.signal_callback_factory_map = {
      "set" : self._set_callback_factory
    }

  def add_upkeep(self, period_ms, callback):
    timer = QtCore.QTimer(self)
    self.upkeep_timer.append(timer)
    timer.start(period_ms)
    timer.timeout.connect(callback)

  def update_text_field(self, item, values=[0.0], config=["{:0.3f}"]):
    pattern = config[0]
    value = values[0]
    if item == None:
      return
    else:
      item.setText(pattern.format(value))

  def update_plot_vec3(self, item, values=vect.Vec3(0,0,0), config=[]):
    if item == None:
      return
    else:
      t = datetime.datetime.now().timestamp() - self.t_start
      item.update_data(t, vect.Vec3(values))

  def set_command_queue(self, queue):
    self.command_queue = queue

  def command_queue_place(self, path, payload):
    self.command_queue.put((path, payload))

  def load_ui_elements(self, ui_element_list, comms, log_entries, widget_settings):
    if log_entries != None:
      log_entries.add('timestamp', self._get_timestamp)

    for idx, ui_element in enumerate(ui_element_list):
      ui = ui_element.Ui(self)
      ui.set_subscriptions(comms.subscribe)
      if log_entries != None:
        ui.add_log_entries(log_entries)
      self.ui_objs.append(ui)

    for element in widget_settings.keys():
      try:
        typeof = eval("QtWidgets."+element)
        for name in widget_settings[element]:
          widget = self.findChild(typeof, name)
          if widget != None:
            fields = widget_settings[element][name]
            self._load_ui_widget(comms, typeof, widget, fields)
      except Exception as e:
        print("Widget interpretation failure\n", e)
        pass


  def _load_ui_widget(self, comms, typeof, widget, fields):
    if "subscriptions" in fields:
      subscriptions = fields["subscriptions"]
      for path in subscriptions.keys():   
        callback = self.callback_map[typeof][subscriptions[path]["callback"]]
        config = subscriptions[path]["config"]
        subscription = WidgetSubscriptionCallback(
          callback,
          widget,
          config
        )
        comms.subscribe(path, subscription.callback)
        self.callback_list.append(subscription)
    
    if "insert" in fields:
      for insert in fields["insert"]:
        self._insert_widget(
          comms,
          widget,
          typeof,
          insert["widget"], 
          insert["settings"], 
          insert["subscriptions"]
        )

    if "signals" in fields:
      for signal in fields["signals"]:
        self._register_signal(
          typeof,
          widget,
          signal,
          fields["signals"][signal]
        )

  def _register_signal(self, typeof, widget, signal, fields):
    callback_factory = self.signal_callback_factory_map[fields["action"]]
    callback = callback_factory(widget, fields)

    setup = self.widget_setup_map[typeof][signal]
    setup(widget, callback)
    
  def _set_callback_factory(self, widget, fields):
    path = fields["path"]
    payload_callbacks = []
    for arg in fields["args"]:
      if isinstance(arg, dict):
        payload_callbacks.append(
          ValueMapCallback(
            self.uiValueMapping, 
            arg["ref"],
            arg["default"]
          ).callback
        )
      else:
        payload_callbacks.append(ValueCallback(arg).callback)
    
    set_callback = SetCallback(
      self.command_queue_place, 
      path, 
      payload_callbacks
    )
    self.callback_list.append(set_callback)
    return set_callback.callback

  def _setup_pressed(self, widget, callback):
    widget.pressed.connect(callback)
  
  def _setup_released(self, widget, callback):
    widget.released.connect(callback)
      

  def _get_timestamp(self):
    return datetime.datetime.now().timestamp()

  def _insert_widget(self, comms, parent_widget, parent_type, widget_str, settings, subscriptions):

    if widget_str == "plotVec3":
      setting_title = settings["title"]
      new_widget = plotCanvas.XyzPlotCanvas(title=setting_title)
      parent_widget.addWidget(new_widget)
    

    for path in subscriptions.keys():
      print(path)  
      callback = self.callback_map[parent_type][subscriptions[path]["callback"]]
      config = subscriptions[path]["config"]
      subscription = WidgetSubscriptionCallback(
        callback,
        new_widget,
        config
      )
      comms.subscribe(path, subscription.callback)
      self.callback_list.append(subscription)
    
    


