class FakeFile:
  def __init__(self):
    self.readData = ""
    self.writeData = ""
    self.closed = False
    self.flushed = False

  def read(self):
    return self.readData

  def readline(self):
    return self.readData
  
  def write(self, str):
    self.writeData += str

  def writelines(self, strs):
    for str in strs:
      self.writeData += str + '\n'

  def flush(self):
    self.flushed = True

  def close(self):
    self.closed = True