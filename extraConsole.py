import sys, io

class extraConsole(io.StringIO):
  def __init__(self, console, add_call):
    self.std = sys.stdout
    self.console = console
    self.add_call = add_call

  def write(self, msg):
    self.std.write(msg)
    if self.console != None:
      self.add_call(self.console, msg)