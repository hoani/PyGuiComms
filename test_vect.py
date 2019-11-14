import vect

class TestVectInitialization:
  def setup_method(self):
    self.vect = vect.Vec3(0,0,0) 

  def test_initialization(self):
    assert(self.vect != None)