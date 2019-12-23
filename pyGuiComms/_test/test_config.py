from pyGuiComms.utilities import vect
import json

class TestConfigLoads:

  def test_protocol(self):
    filepath = 'config/protocol.json'
    try:
      with open(filepath, 'r') as f:
        loaded = json.load(f)
    except:
      assert(False)


