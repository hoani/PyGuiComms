from pyGuiComms.utilities import vect
import json

class TestConfigParses:

  def test_protocol(self):
    filepath = 'config/protocol.json'
    try:
      with open(filepath, 'r') as f:
        loaded = json.load(f)
    except:
      assert(False)

  def test_settings(self):
    filepath = 'config/settings.json'
    try:
      with open(filepath, 'r') as f:
        loaded = json.load(f)
    except:
      assert(False)

  def test_widgets(self):
    filepath = 'config/widgets.json'
    try:
      with open(filepath, 'r') as f:
        loaded = json.load(f)
    except:
      assert(False)


