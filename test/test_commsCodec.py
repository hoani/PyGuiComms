from source.utilities import commsCodec
import json

class TestCountToPath():
  def setup_method(self):
    self.root = { "_addr": "0000",
      "NZ": {
        "Auckland": {
          "GlenInnes": { "type": "u16", "set": False },
          "Avondale": { "type": "float", "set": True}
        },
        "Hamilton": {"type": "u8", "set": True },
        "Napier": { "type": "bool", "set": False }
      },
      "Rarotonga": { "type": "i32", "set": True }
    }

  def test_none_counts_depth(self):
    expected = 7
    result = commsCodec.count_to_path(self.root, None)
    assert(result == expected)

  def test_basic_one_deep(self):
    expected = 1
    result = commsCodec.count_to_path(self.root, ["NZ"])
    assert(result == expected)

  def test_basic_two_deep(self):
    expected = 2
    result = commsCodec.count_to_path(self.root, ["NZ", "Auckland"])
    assert(result == expected)

  def test_basic_three_deep(self):
    expected = 3
    result = commsCodec.count_to_path(self.root, ["NZ", "Auckland", "GlenInnes"])
    assert(result == expected)

  def test_three_deep(self):
    expected = 4
    result = commsCodec.count_to_path(self.root, ["NZ", "Auckland", "Avondale"])
    assert(result == expected)

  def test_two_deep(self):
    expected = 6
    result = commsCodec.count_to_path(self.root, ["NZ", "Napier"])
    assert(result == expected)

  def test_incorrect_path(self):
    expected = None
    result = commsCodec.count_to_path(self.root, ["NZ", "Christchurch"])
    assert(result == expected)

class TestGetPacketEncode():

  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)
    
    with open(protocol_file_path, "r") as protocol_file:
      self.settings = json.load(protocol_file)

  def test_simple_encoding(self):
    expected = ("G0000\n").encode('utf-8')
    packet = commsCodec.Packet("get", "protocol")
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_nested_encoding(self):
    expected = ("G0005\n").encode('utf-8')
    packet = commsCodec.Packet("get", "protocol/version/patch")
    result = self.codec.encode(packet)
    assert(result == expected)

