class Vec3():

  def __init__(self, x, y=None, z=None):
    if y == None and z == None:
      if isinstance(x, list) and len(x) == 3:
        self.x = x[0]
        self.y = x[1]
        self.z = x[2]
      else:
        self.x = x
        self.y = x
        self.z = x
    else:
      self.x = x
      self.y = y
      self.z = z