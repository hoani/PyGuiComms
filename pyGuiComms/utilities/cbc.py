# Callback classes utility
#
# Provides a series of class methods with callback function


class ValueCallback:
  def __init__(self, value):
    self._value = value

  def callback(self):
    return self._value


class InjectValueCallback:
  def __init__(self, callback, value):
    self._callback = callback
    self._value = value

  def callback(self):
    self._callback(self._value)


class MapGetterCallback:
  def __init__(self, my_map, key, default=None):
    self._map = my_map
    self._key = key
    self._default = default

  def callback(self):
    if self._key in self._map:
      return self._map[self._key]
    else:
      return self._default


class MapSetterCallback:
  def __init__(self, my_map, key, value_callback, multiplier):
    self._map = my_map
    self._value_callback = value_callback
    self._key = key
    self._multiplier = multiplier
    if self._key not in self._map:
      self.callback()

  def callback(self):
    value = self._value_callback()
    
    if self._multiplier != None:
      value = value * self._multiplier

    self._map[self._key] = value



class PeriodicCallback:
  def __init__(self, period_ms, callback, set_interval):
    self._period_ms = period_ms
    self._callback = callback
    self._set_interval = set_interval
    self._timer = None

  def start(self):
    if (self._timer == None):
      self._timer = self._set_interval(self._period_ms, self._callback)
    else:
      self._timer.start(self._period_ms)
    self.callback()

  def stop(self):
    self._timer.stop()

  def callback(self):
    self._callback()
