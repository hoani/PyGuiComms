from pyGuiComms.utilities import cbc

class TestCbcValueCallback:
  def test_initialization(self):
    cbo = cbc.ValueCallback(12)
    assert(cbo != None)

  def test_simple_callback(self):
    cbo = cbc.ValueCallback(12)
    assert(cbo.callback() == 12)


class TestInjectValueCallback:
  def setup_method(self):
    self.value = None

  def callback(self, value):
    self.value = value

  def test_initialization(self):
    cbo = cbc.InjectValueCallback(self.callback, 1337)
    assert(cbo != None)

  def test_executes_callback(self):
    expected = 1337
    cbo = cbc.InjectValueCallback(self.callback, expected)
    cbo.callback()
    assert(self.value == expected)

class TestMapGetterCallback:
  def setup_method(self):
    self.map = {
      "string": "Hello World",
      "one": 1,
      "two": 2
    }

  def test_initialization(self):
    cbo = cbc.MapGetterCallback(self.map, "string", "Bye World")
    assert(cbo != None)

  def test_returns_correct_value(self):
    cbo = cbc.MapGetterCallback(self.map, "string", "Bye World")
    assert(cbo.callback() == "Hello World")

  def test_returns_default_value(self):
    cbo = cbc.MapGetterCallback(self.map, "invalid", "default-value")
    assert(cbo.callback() == "default-value")


class TestMapSetterCallback:
  def setup_method(self):
    self.map = {
      "string": "Hello World",
      "one": 1,
      "two": 2
    }
    self.value = None

  def value_callback(self):
    return self.value

  def test_initialization(self):
    cbo = cbc.MapSetterCallback(self.map, "one", self.value_callback, 1.0)
    assert(cbo != None)

  def test_sets_map_value(self):
    cbo = cbc.MapSetterCallback(self.map, "one", self.value_callback, 1.0)
    self.value = 11
    cbo.callback()
    assert(self.map["one"] == self.value)

  def test_creates_map_key_if_required(self):
    self.value = 3
    cbo = cbc.MapSetterCallback(self.map, "three", self.value_callback, 1.0)
    assert(self.map["three"] == self.value)

  def test_multiplies_value(self):
    cbo = cbc.MapSetterCallback(self.map, "one", self.value_callback, -2.0)
    self.value = 11
    cbo.callback()
    assert(self.map["one"] == -22)


class TimerMock:
  def __init__(self):
    self.ms = None
    self.started = False
    self.stopped = False

  def start(self, ms):
    self.ms = ms
    self.started = True

  def stop(self):
    self.stopped = True


class TestPeriodicCallback:
  def setup_method(self):
    self.callback_called = False
    self.timer = TimerMock()
    self.set_interval_called = False
    self.interval_ms = None
    self.interval_callback = None

  def my_callback(self):
    self.callback_called = True

  def set_interval(self, ms, callback):
    self.set_interval_called = True
    self.interval_ms = ms
    self.interval_callback = callback
    return self.timer

  def test_initialization(self):
    cbo = cbc.PeriodicCallback(100, self.my_callback, self.set_interval)
    assert(cbo != None)

  def test_callback_executes_callback(self):
    cbo = cbc.PeriodicCallback(100, self.my_callback, self.set_interval)
    cbo.callback()
    assert(self.callback_called)

  def test_callback_start(self):
    cbo = cbc.PeriodicCallback(100, self.my_callback, self.set_interval)
    cbo.start()
    assert(self.set_interval_called)
    assert(self.interval_ms == 100)
    assert(self.interval_callback == self.my_callback)
    assert(self.callback_called)

  def test_callback_stop(self):
    cbo = cbc.PeriodicCallback(100, self.my_callback, self.set_interval)
    cbo.start()
    cbo.stop()
    assert(self.timer.stopped)

  def test_callback_start_only_requests_timer_once(self):
    cbo = cbc.PeriodicCallback(100, self.my_callback, self.set_interval)
    cbo.start()
    self.set_interval_called = False
    self.timer.started = False
    cbo.start()
    assert(self.set_interval_called == False)
    assert(self.timer.started == True)
    assert(self.timer.ms == 100)





