from source.utilities import logger
from test.fakes import fakeFile

intValue = 0
floatValue = 3.14
strValue = "StrData"
strValue2 = "StrData2"

def callback_string():
  global strValue
  return strValue

def callback_string2():
  global strValue2
  return strValue2

def callback_integer():
  global intValue
  return intValue

def callback_float():
  global floatValue
  return floatValue

def reset_callback_values():
  global intValue
  global floatValue
  global strValue 
  global strValue2 
  intValue = 0
  floatValue = 3.14
  strValue = "StrData"
  strValue2 = "StrData2"



class TestLoggerInitialization:
  def setup_method(self):
    self.logFile = fakeFile.FakeFile()
    self.logEntries = logger.LogEntries()
    reset_callback_values() 

  def test_initialization(self):
    log = logger.Logger(self.logFile, self.logEntries)
    assert(log != None)

  def test_loggerCopiesTheEntriesList(self):
    self.logEntries["Test"] = callback_string
    log = logger.Logger(self.logFile, self.logEntries)
    self.logEntries["Test"] = callback_string2
    
    assert(log.entries["Test"]() == callback_string())

  def test_loggerWritesHeadings(self):
    keys = ["Test", "Test1", "Test2"]
    for key in keys:
      self.logEntries.add(key, callback_string)
    log = logger.Logger(self.logFile, self.logEntries)
    
    expected = "Test,Test1,Test2\n"
    assert(expected == self.logFile.writeData)

class TestLoggerPublish:
  def setup_method(self):
    self.logFile = fakeFile.FakeFile()
    self.logEntries = logger.LogEntries()
    reset_callback_values()

  def test_loggerWritesData(self):
    self.logEntries.add("Test", callback_string)
    log = logger.Logger(self.logFile, self.logEntries)
    
    log.publish()
    expected = "Test\nStrData\n"
    assert(expected == self.logFile.writeData)

  def test_loggerPublishInvokesFlush(self):
    self.logEntries.add("Test", callback_string)
    log = logger.Logger(self.logFile, self.logEntries)
    
    log.publish()
    assert(self.logFile.flushed)

  def test_loggerWritesCSVRow(self):
    self.logEntries.add("Test", callback_string)
    self.logEntries.add("Test1", callback_string2)
    log = logger.Logger(self.logFile, self.logEntries)
    
    log.publish()
    expected = "Test,Test1\nStrData,StrData2\n"
    assert(expected == self.logFile.writeData)

  def test_logEntriesOrder(self): 
    self.logEntries.add("Test1", callback_string2)
    self.logEntries.add("Test", callback_string)
    log = logger.Logger(self.logFile, self.logEntries)
    
    log.publish()
    expected = "Test1,Test\nStrData2,StrData\n"
    assert(expected == self.logFile.writeData)

  def test_loggerWritesMultipleCSVRows(self):
    global intValue
    self.logEntries.add("Index", callback_integer)
    self.logEntries.add("Test", callback_string)
    self.logEntries.add("Test1", callback_string2)
    log = logger.Logger(self.logFile, self.logEntries)
    
    intValue = 1
    log.publish()
    intValue = 2
    log.publish()
    expected = "Index,Test,Test1\n1,StrData,StrData2\n2,StrData,StrData2\n"
    assert(expected == self.logFile.writeData)




# Log Entries
class TestLogEntries:
  def setup_method(self):
    self.logEntries = logger.LogEntries()
    reset_callback_values()

  def test_initialization(self):
    assert(self.logEntries != None)

  def test_addEntry(self):
    key = "Test"
    self.logEntries.add(key, callback_string)
    assert(self.logEntries[key] != None)

  def test_addEntries(self):
    keys = ["Test", "Test1", "Test2"]
    for key in keys:
      self.logEntries.add(key, callback_string)
    
    for key in keys:
      assert(key in self.logEntries.keys())

  def test_getSingle(self):
    key = "Test"
    self.logEntries.add(key, callback_string)

    values = self.logEntries.get()
    expected = callback_string()

    assert(values[key] == expected)

  def test_getSingleInteger(self):
    key = "Test"
    self.logEntries.add(key, callback_integer)

    values = self.logEntries.get()
    expected = str(callback_integer())

    assert(values[key] == expected)

  def test_getSingleFloat(self):
    key = "Test"
    self.logEntries.add(key, callback_float)

    values = self.logEntries.get()
    expected = str(callback_float())

    assert(values[key] == expected)

  def test_getMultiple(self):
    keys = ["Test", "Test1", "Test2"]
    for key in keys:
      self.logEntries.add(key, callback_string)

    values = self.logEntries.get()
    expected = callback_string()

    for key in keys:
      assert(values[key] == expected)

