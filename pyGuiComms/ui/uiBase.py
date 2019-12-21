# Author: Hoani Bryson
#
# UI Base - Binds UI control to a QT mainWindow object
#  from a configuration map

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from pyGuiComms.utilities import vect, cbc, debug
from pyGuiComms.ui import plotCanvas, extraConsole
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


class WidgetSubscriptionCallback:
  def __init__(self, callback, widget, config):
    self._callback = callback
    self._widget = widget
    self._config = config

  def callback(self, values):
    self._callback(self._widget, values, self._config)


class SetCallback:
  def __init__(self, queue_callback, path, payload_callbacks, kvmap):
    self._callback = queue_callback
    self._path = path
    self._payload_callbacks = payload_callbacks
    self._map = kvmap

    if len(payload_callbacks) == 1:
      self._map[self._path] = payload_callbacks[0]()

  def callback(self):
    payload = []
    for callback in self._payload_callbacks:
      payload.append(callback())

    self._callback(self._path, tuple(payload))

    # TODO, need a nice way to dig into paths and set multi-item paths
    if len(payload) == 1:
      self._map[self._path] = payload[0]


class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.show()
    self.t_start = datetime.datetime.now().timestamp()
    self.command_queue = None
    self.upkeep_timer = []
    self.callback_list = [] # This is used to avoid garbage collection
    try:
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    except:
        pass

    self.key_value_map = {}

    self.subscription_callback_map = {
      QtWidgets.QLineEdit: {
        "set": self.update_text_field
      },
      QtWidgets.QBoxLayout: {
        "setVec3": self.update_plot_vec3,
        "setSingle": self.update_plot_single,
      }
    }

    self.widget_setup_map = {
      QtWidgets.QPushButton: {
        "pressed": self._setup_pressed,
        "released": self._setup_released
      },
      QtWidgets.QSlider: {
        "released": self._setup_slider_released
      }
    }

    self.signal_callback_factory_map = {
      "set" : self._set_callback_factory,
      "map" : self._map_callback_factory
    }

  
  def get_data_map(self):
    return self.key_value_map


  def load(self, comms, widget_settings):
    for element in widget_settings.keys():
      try:
        typeof = eval("QtWidgets."+element)
        for name in widget_settings[element]:
          widget = self.findChild(typeof, name)
          if widget != None:
            fields = widget_settings[element][name]
            self._load_ui_widget(comms, typeof, widget, fields)
      except Exception as e:
        print("Widget interpretation failure\n")
        debug.print_exception(e)


  def set_command_queue(self, queue):
    self.command_queue = queue


  def add_upkeep(self, period_ms, callback):
    timer = QtCore.QTimer(self)
    self.upkeep_timer.append(timer)
    timer.start(period_ms)
    timer.timeout.connect(callback)
    return timer


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


  def update_plot_single(self, item, values=0, config=[]):
    if item == None:
      return
    else:
      t = datetime.datetime.now().timestamp() - self.t_start
      item.update_data(t, values)


  def _load_ui_widget(self, comms, typeof, widget, fields):
    try:
      if "stream" in fields:
        if fields["stream"]["target"] == "stdout":
          sys.stdout = extraConsole.extraConsole(widget, typeof.insertPlainText)
          callback = cbc.InjectValueCallback(widget.moveCursor, QtGui.QTextCursor.End)
          widget.textChanged.connect(callback.callback)
          self.callback_list.append(callback)

      if "subscriptions" in fields:
        subscriptions = fields["subscriptions"]
        for path in subscriptions.keys():
          callback = self.subscription_callback_map[typeof][subscriptions[path]["callback"]]
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
        for signal in fields["signals"].keys():
          if isinstance(fields["signals"][signal], list) == False:
            fields["signals"][signal] = [fields["signals"][signal]] 

          for items in fields["signals"][signal]:
            if isinstance(items, list) == False:
              items = [items]
            
            for item in items:
              self._register_signal(
                typeof,
                widget,
                signal,
                item
              )

    except Exception as e:
      print("Widget interpretation failure\n")
      debug.print_exception(e)

  def _register_signal(self, typeof, widget, signal, fields):
    callback_factory = self.signal_callback_factory_map[fields["action"]]
    callback = callback_factory(widget, fields)
    setup = self.widget_setup_map[typeof][signal]

    if "repeat" in fields:
      params = fields["repeat"]
      period_ms = params["rate"] * 1000

      stop_signal = params["stop"]
      stop_setup = self.widget_setup_map[typeof][stop_signal]

      periodic = cbc.PeriodicCallback(period_ms, callback, self.add_upkeep)
      self.callback_list.append(periodic)

      setup(widget, periodic.start)
      stop_setup(widget, periodic.stop)
    else:
      setup(widget, callback)


  def _set_callback_factory(self, widget, fields):
    path = fields["path"]
    payload_callbacks = []
    for arg in fields["args"]:
      if isinstance(arg, dict):
        pl_callback = cbc.MapGetterCallback(
            self.key_value_map,
            arg["key"],
            arg["default"]
          )
        payload_callbacks.append(
          pl_callback.callback
        )
        self.callback_list.append(pl_callback)
      else:
        payload_callbacks.append(cbc.ValueCallback(arg).callback)

    set_callback = SetCallback(
      self._command_queue_place,
      path,
      payload_callbacks,
      self.key_value_map
    )
    self.callback_list.append(set_callback)
    return set_callback.callback


  def _command_queue_place(self, path, payload):
    self.command_queue.put((path, payload))


  def _map_callback_factory(self, widget, fields):
    key = fields["key"]
    multiplier = fields["multiplier"]

    map_callback = cbc.MapSetterCallback(
      self.key_value_map,
      key,
      widget.value,
      multiplier
    )

    self.callback_list.append(map_callback)
    return map_callback.callback

  def _setup_pressed(self, widget, callback):
    widget.pressed.connect(callback)

  def _setup_released(self, widget, callback):
    widget.released.connect(callback)

  def _setup_slider_released(self, widget, callback):
    widget.sliderReleased.connect(callback)


  def _get_timestamp(self):
    return datetime.datetime.now().timestamp()

  def _insert_widget(self, comms, parent_widget, parent_type, widget_str, settings, subscriptions):

    if widget_str == "plotVec3":
      setting_title = settings["title"]
      new_widget = plotCanvas.XyzPlotCanvas(title=setting_title)
      parent_widget.addWidget(new_widget)

    if widget_str == "plotSingle":
      setting_title = settings["title"]
      new_widget = plotCanvas.SinglePlotCanvas(title=setting_title)
      parent_widget.addWidget(new_widget)


    for path in subscriptions.keys():
      callback = self.subscription_callback_map[parent_type][subscriptions[path]["callback"]]
      config = subscriptions[path]["config"]
      subscription = WidgetSubscriptionCallback(
        callback,
        new_widget,
        config
      )
      comms.subscribe(path, subscription.callback)
      self.callback_list.append(subscription)

  def _console_cursor(self):
    self.console.moveCursor(QtGui.QTextCursor.End)




