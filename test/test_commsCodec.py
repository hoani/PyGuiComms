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

  def test_zero_counts(self):
    expected = []
    expected_count = 0
    (result, result_count) = commsCodec.path_from_count(self.root, 0)
    assert(result == expected)
    assert(result_count == expected_count)

  def test_simple_counts(self):
    expected = ["NZ", "Auckland", "Avondale"]
    expected_count = 0
    (result, result_count) = commsCodec.path_from_count(self.root, 4)
    assert(result == expected)
    assert(result_count == expected_count)

  def test_complex_counts(self):
    expected = ["NZ", "Napier"]
    expected_count = 0
    (result, result_count) = commsCodec.path_from_count(self.root, 6)
    assert(result == expected)
    assert(result_count == expected_count)

  def test_no_result(self):
    expected = []
    expected_count = 3
    (result, result_count) = commsCodec.path_from_count(self.root, 10)
    assert(result == expected)
    assert(result_count == expected_count)


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


class TestFromAddress():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_address_map(self):
    assert("0000" in self.codec.address_map.keys())
    assert("1000" in self.codec.address_map.keys())
    assert("1100" in self.codec.address_map.keys())
    assert("2000" in self.codec.address_map.keys())
    assert("8000" in self.codec.address_map.keys())
    assert("1200" in self.codec.address_map.keys())
    assert(self.codec.address_map["0000"] == "protocol")
    assert(self.codec.address_map["1000"] == "ping")
    assert(self.codec.address_map["1100"] == "health")
    assert(self.codec.address_map["2000"] == "typecheck")
    assert(self.codec.address_map["8000"] == "control")
    assert(self.codec.address_map["1200"] == "imu")

  def test_mapped_root_path_from_address(self):
    expected = "protocol"
    result = self.codec.path_from_address("0000")
    assert(expected == result)

  def test_mapped_root_struct_from_address(self):
    expected = self.codec.protocol["data"]["protocol"]
    result = self.codec.struct_from_address("0000")
    assert(expected == result)

  def test_mapped_path_from_address(self):
    expected = "protocol/version"
    result = self.codec.path_from_address("0001")
    assert(expected == result)

  def test_mapped_complex_path_from_address(self):
    expected = "control/manual/speed"
    result = self.codec.path_from_address("8004")
    assert(expected == result)

  def test_no_path(self):
    expected = ""
    result = self.codec.path_from_address("9000")
    assert(expected == result)
  
  def test_invalid_path(self):
    expected = ""
    result = self.codec.path_from_address("invalid")
    assert(expected == result)

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

class TestGetPacketDecode():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_simple_decoding(self):
    expected = commsCodec.Packet("get", "protocol")
    result = self.codec.decode("G0000\n".encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
  
  def test_nested_decoding(self):
    expected = commsCodec.Packet("get", "protocol/version/patch")
    result = self.codec.decode("G0004\n".encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)

  def test_deep_nest_decoding(self):
    expected = commsCodec.Packet("get", "control/pid/setpoint/value")
    result = self.codec.decode("G800e\n".encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)

  def test_ack_category(self):
    expected = commsCodec.Packet("ack")
    result = self.codec.decode("A\n".encode('utf-8'))
    assert(result.category == expected.category)
  
  def test_nack_category(self):
    expected = commsCodec.Packet("nak")
    result = self.codec.decode("N\n".encode('utf-8'))
    assert(result.category == expected.category)

  def test_simple_packet_decoding(self):
    expected = commsCodec.Packet("get", "protocol/version/major", tuple([0x11]))
    result = self.codec.decode("G0002:11\n".encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload[0] == expected.payload[0])

  def test_multi_packet_decoding(self):
    expected = commsCodec.Packet("get", "protocol/version", tuple([0x11, 0x22, 0x3344]))
    result = self.codec.decode("G0001:11:22:3344\n".encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)


class TestSetPacketEncodeMultiple():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_sequential(self):
    expected = ("S0001:12:34:0567\n").encode('utf-8')
    packet = commsCodec.Packet("set", "protocol/version", tuple([0x12, 0x34, 0x567]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_non_sequential(self):
    expected = ("S0000:12:34:0567:Hoani\n").encode('utf-8')
    packet = commsCodec.Packet("set", "protocol", tuple([0x12, 0x34, 0x567, "Hoani"]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_ignores_unused_payload_items(self):
    expected = ("S0001:12:34:0567\n").encode('utf-8')
    packet = commsCodec.Packet("set", "protocol/version", tuple([0x12, 0x34, 0x567]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_ignores_unused_sequential_items(self):
    expected = ("S0001:12:34\n").encode('utf-8')
    packet = commsCodec.Packet("set", "protocol/version", tuple([0x12, 0x34]))
    result = self.codec.encode(packet)
    assert(result == expected)


class TestSetPacketDecodeMultiple():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_sequential(self):
    expected = commsCodec.Packet("set", "protocol/version", tuple([0x12, 0x34, 0x567]))
    result = self.codec.decode(("S0001:12:34:0567\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_non_sequential(self):
    expected = commsCodec.Packet("set", "protocol", tuple([0x12, 0x34, 0x567, "Hoani"]))
    result = self.codec.decode(("S0000:12:34:0567:Hoani\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_ignores_unused_payload_items(self):
    expected = commsCodec.Packet("set", "protocol/version", tuple([0x12, 0x34, 0x567]))
    result = self.codec.decode(("S0001:12:34:0567\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_ignores_unused_sequential_items(self):
    expected = commsCodec.Packet("set", "protocol/version", tuple([0x12, 0x34]))
    result = self.codec.decode(("S0001:12:34\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

class TestSetPacketEncodeSingle():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_simple_string(self):
    expected = ("S2001:Hoani's String\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/string", tuple(["Hoani's String"]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_bool(self):
    expected = ("S2002:1\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/boolean", tuple([True]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_u8(self):
    expected = ("S2003:a5\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint8", tuple([0xa5]))
    result = self.codec.encode(packet)
    assert(result == expected)
  
  def test_underflow_u8(self):
    expected = ("S2003:00\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint8", tuple([-0xa5]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_overflow_u8(self):
    expected = ("S2003:ff\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint8", tuple([0x1a5]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_u16(self):
    expected = ("S2004:0234\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint16", tuple([0x0234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_underflow_u16(self):
    expected = ("S2004:0000\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint16", tuple([-0x0234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_overflow_u16(self):
    expected = ("S2004:ffff\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint16", tuple([0x10234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_u32(self):
    expected = ("S2005:00102234\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint32", tuple([0x102234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_underflow_u32(self):
    expected = ("S2005:00000000\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint32", tuple([-0x102234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_overflow_u32(self):
    expected = ("S2005:ffffffff\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint32", tuple([0x100002234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_u64(self):
    expected = ("S2006:0010223400000078\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint64", tuple([0x10223400000078]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_underflow_u64(self):
    expected = ("S2006:0000000000000000\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint64", tuple([-0x10223400000078]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_overflow_u64(self):
    expected = ("S2006:ffffffffffffffff\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/uint64", tuple([0x10000010223400000078]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_i8(self):
    expected = ("S2007:11\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int8", tuple([0x11]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_negative_i8(self):
    expected = ("S2007:ef\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int8", tuple([-0x11]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_i16(self):
    expected = ("S2008:0234\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int16", tuple([0x0234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_signed_i16(self):
    expected = ("S2008:fdcc\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int16", tuple([-0x0234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_i32(self):
    expected = ("S2009:00102234\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int32", tuple([0x102234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_signed_i32(self):
    expected = ("S2009:ffefddcc\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int32", tuple([-0x102234]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_simple_i64(self):
    expected = ("S200a:0010223400000078\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int64", tuple([0x10223400000078]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_signed_i64(self):
    expected = ("S200a:ffefddcbffffff88\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/int64", tuple([-0x10223400000078]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_float(self):
    expected = ("S200b:60dc9cc9\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/float", tuple([1.2717441261e+20]))
    result = self.codec.encode(packet)
    assert(result == expected)

  def test_double(self):
    expected = ("S200c:3ff3c083126e978d\n").encode('utf-8')
    packet = commsCodec.Packet("set", "typecheck/double", tuple([1.2344999999999999307]))
    result = self.codec.encode(packet)
    assert(result == expected)

###########
class TestSetPacketDecodeSingle():
  def setup_method(self):
    protocol_file_path = "test/fakes/protocol.json"
    self.codec = commsCodec.Codec(protocol_file_path)

  def test_simple_string(self):
    expected = commsCodec.Packet("set", "typecheck/string", tuple(["Hoani's String"]))
    result = self.codec.decode(("S2001:Hoani's String\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_bool(self):
    expected = commsCodec.Packet("set", "typecheck/boolean", tuple([True]))
    result = self.codec.decode(("S2002:1\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_u8(self):
    expected = commsCodec.Packet("set", "typecheck/uint8", tuple([0xa5]))
    result = self.codec.decode(("S2003:a5\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)
  
  def test_underflow_u8(self):
    expected = commsCodec.Packet("set", "typecheck/uint8", tuple([0x00]))
    result = self.codec.decode(("S2003:-e3\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_overflow_u8(self):
    expected = commsCodec.Packet("set", "typecheck/uint8", tuple([0xff]))
    result = self.codec.decode(("S2003:1a5\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_u16(self):
    expected = commsCodec.Packet("set", "typecheck/uint16", tuple([0x0234]))
    result = self.codec.decode(("S2004:0234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_underflow_u16(self):
    expected = commsCodec.Packet("set", "typecheck/uint16", tuple([0x0000]))
    result = self.codec.decode(("S2004:-0234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_overflow_u16(self):
    expected = commsCodec.Packet("set", "typecheck/uint16", tuple([0xffff]))
    result = self.codec.decode(("S2004:1ffff\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_u32(self):
    expected = commsCodec.Packet("set", "typecheck/uint32", tuple([0x102234]))
    result = self.codec.decode(("S2005:00102234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_underflow_u32(self):
    expected = commsCodec.Packet("set", "typecheck/uint32", tuple([0x00000000]))
    result = self.codec.decode(("S2005:-00102234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_overflow_u32(self):
    expected = commsCodec.Packet("set", "typecheck/uint32", tuple([0xffffffff]))
    result = self.codec.decode(("S2005:100002234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_u64(self):
    expected = commsCodec.Packet("set", "typecheck/uint64", tuple([0x10223400000078]))
    result = self.codec.decode(("S2006:0010223400000078\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_underflow_u64(self):
    expected = commsCodec.Packet("set", "typecheck/uint64", tuple([0x0]))
    result = self.codec.decode(("S2006:-10223400000078\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_overflow_u64(self):
    expected = commsCodec.Packet("set", "typecheck/uint64", tuple([0xffffffffffffffff]))
    result = self.codec.decode(("S2006:10000010223400000078\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_i8(self):
    expected = commsCodec.Packet("set", "typecheck/int8", tuple([0x11]))
    result = self.codec.decode(("S2007:11\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_negative_i8(self):
    expected = commsCodec.Packet("set", "typecheck/int8", tuple([-0x11]))
    result = self.codec.decode(("S2007:ef\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_i16(self):
    expected = commsCodec.Packet("set", "typecheck/int16", tuple([0x0234]))
    result = self.codec.decode(("S2008:0234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_signed_i16(self):
    expected = commsCodec.Packet("set", "typecheck/int16", tuple([-0x0234]))
    result = self.codec.decode(("S2008:fdcc\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_i32(self):
    expected = commsCodec.Packet("set", "typecheck/int32", tuple([0x102234]))
    result = self.codec.decode(("S2009:00102234\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_signed_i32(self):
    expected = commsCodec.Packet("set", "typecheck/int32", tuple([-0x102234]))
    result = self.codec.decode(("S2009:ffefddcc\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_simple_i64(self):
    expected = commsCodec.Packet("set", "typecheck/int64", tuple([0x10223400000078]))
    result = self.codec.decode(("S200a:0010223400000078\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_signed_i64(self):
    expected = commsCodec.Packet("set", "typecheck/int64", tuple([-0x10223400000078]))
    result = self.codec.decode(("S200a:ffefddcbffffff88\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(result.payload == expected.payload)

  def test_float(self):
    expected = commsCodec.Packet("set", "typecheck/float", tuple([1.2717441261e+20]))
    result = self.codec.decode(("S200b:60dc9cc9\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(abs(result.payload[0] - expected.payload[0]) < 0.00001e+20)

  def test_double(self):
    expected = commsCodec.Packet("set", "typecheck/double", tuple([1.2344999999999999307]))
    result = self.codec.decode(("S200c:3ff3c083126e978d\n").encode('utf-8'))
    assert(result.category == expected.category)
    assert(result.path == expected.path)
    assert(abs(result.payload[0] - expected.payload[0]) < 0.0000001 )

