from source.utilities import commsCodec
import json

class TestGetStruct():
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

  def test_get_none(self):
    expected = None
    result = commsCodec.get_struct(self.root, ["Florida"])
    assert(result == expected)
  
  def test_get_basic(self):
    expected = self.root["NZ"]
    result = commsCodec.get_struct(self.root, ["NZ"])
    assert(result == expected)

  def test_get_deep(self):
    expected = self.root["NZ"]["Auckland"]["Avondale"]
    result = commsCodec.get_struct(self.root, ["NZ", "Auckland", "Avondale"])
    assert(result == expected)

  def test_get_another(self):
    expected = self.root["NZ"]["Napier"]
    result = commsCodec.get_struct(self.root, ["NZ", "Napier"])
    assert(result == expected)

  def test_no_path(self):
    expected = self.root
    result = commsCodec.get_struct(self.root, [])
    assert(result == expected)

class TestExtractTypes():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    codec = commsCodec.Codec(protocol_file_path)
    self.data = codec.protocol["data"]

  def test_simple_type(self):
    expected = ["bool"]
    result = commsCodec.extract_types(self.data, ["ping"])
    assert(result == expected)

  def test_nested_type(self):
    expected = ["u16"]
    result = commsCodec.extract_types(self.data, ["protocol", "version", "patch"])
    assert(result == expected)

  def test_multiple_types(self):
    expected = ["u8", "u8", "u16"]
    result = commsCodec.extract_types(self.data, ["protocol", "version"])
    assert(result == expected)

  def test_multiple_types_nesting(self):
    expected = ["u8", "u8", "u16", "string"]
    result = commsCodec.extract_types(self.data, ["protocol"])
    assert(result == expected)



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

class TestAckPacketEncode():

  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_ack_encoding(self):
    expected = ("A\n").encode('utf-8')
    packet = commsCodec.Packet("ack")
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_nack_encoding(self):
    expected = ("N\n").encode('utf-8')
    packet = commsCodec.Packet("nak")
    result = self.codec.encode(packet)
    assert(result == expected)


class TestGetPacketEncode():

  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_simple_encoding(self):
    expected = ("G0000\n").encode('utf-8')
    packet = commsCodec.Packet("get", "protocol")
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_nested_encoding(self):
    expected = ("G0004\n").encode('utf-8')
    packet = commsCodec.Packet("get", "protocol/version/patch")
    result = self.codec.encode(packet)
    assert(result == expected)


class TestSetPacketEncode():

  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_simple_u8(self):
    expected = ("S2003:a5\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint8", tuple([0xa5]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_u16(self):
    expected = ("S2004:0234\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint16", tuple([0x0234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_u32(self):
    expected = ("S2005:00102234\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint32", tuple([0x102234]))
    result = self.codec.encode(packet)
    assert(result == expected)
  # todo: Strings, u16, u32, u64, u128, i16, i32, i64, i128, floats, booleans

