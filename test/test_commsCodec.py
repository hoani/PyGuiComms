from source.utilities import commsCodec
import json

class TestCommandPacketEncode():

  def setup_method(self):
    protocol_file_path = "json/protocol.json"
    protocol = commsCodec.get_codec_protocol(protocol_file_path)
    self.packetFactory = commsCodec.PacketFactory(protocol)
    
    with open(protocol_file_path, "r") as protocol_file:
      self.settings = json.load(protocol_file)

  def test_simple_encoding(self):
    expected = ("c"+self.settings["command"]["items"]["disable"]["encode"]+"\n").encode('utf-8')
    packet = self.packetFactory.CommandPacket("disable")
    result = packet.encode()
    assert(result == expected)

  def test_integer_payload_encoding(self):
    expected = ("c"+self.settings["command"]["items"]["request"]["encode"]+"0000"+"\n").encode('utf-8')
    packet = self.packetFactory.RequestPacket("ping")
    result = packet.encode()
    assert(result == expected)

