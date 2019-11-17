

class LogEntries(dict):
  def Add(self, key, callback):
    self[key] = callback

  def Get(self):
    values = {}
    for key in self.keys():
      callback = self[key]
      values[key] = str(callback())

    return values

class Logger:
  def __init__(self, file, entries):
    self.file = file
    self.entries = LogEntries(entries)
    
    header = ""
    for key in self.entries.keys():
      header += key + ","

    header = header[0:-1] + '\n'
    self.file.write(header)

  def Publish(self):
    line = ""
    # Note: as of python 3.7 a dict is guaranteed to have insertion-order preservation
    values = self.entries.Get()
    for key in self.entries.keys():
      line += values[key] + ","

    line = line[0:-1] + '\n'
    self.file.write(line)
    self.file.flush()


if __name__ == "__main__":
  pass