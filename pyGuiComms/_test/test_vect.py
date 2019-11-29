from pyGuiComms.utilities import vect

class TestVectBasic:

  def test_initialization(self):
    self.vect = vect.Vec3(0,0,0) 
    assert(self.vect != None)

  def test_values(self):
    self.vect = vect.Vec3(-123,0,789) 
    assert(self.vect.x == -123)
    assert(self.vect.y == 0)
    assert(self.vect.z == 789)

