
import json


def get_codec_protocol(protocol_file_path):
  with open(protocol_file_path, "r") as protocol_file:
    proto = json.load(protocol_file)
  return proto

class PacketFactory():
  def __init__(self, packet_protocol):
    self.protocol = packet_protocol

  def CommandPacket(self, command):
    packet = Packet(self.protocol["command"], command)
    return packet

  def RequestPacket(self, item):
    packet = Packet(self.protocol["command"], "request", self.protocol["data"]["items"][item]["encode"])
    return packet

class Packet():
  def __init__(self, packet_protocol, item, payload=None):
    self.protocol = packet_protocol
    self.item = item
    self.payload = payload

  def encode(self):
    encoded = self.protocol["encode"]
    if self.item in self.protocol["items"]:
      encoded += self.protocol["items"][self.item]["encode"]
      encoded += self._encode_payload()
      encoded += '\n'
      return encoded.encode('utf-8')
    
    return None

  def _encode_payload(self):
    encoded = ""
    if self.payload != None:
      for datum in self.payload:
        encoded += self._encode_payload_datum(datum)
    return encoded

  def _encode_payload_datum(self, datum):
    if isinstance(datum, str):
      return datum


class CommandDecoder():
  def __init__(self, command_protocol):
    self.protocol = command_protocol
    self.bytes = b''
    
  def decode(self):
    pass

class Codec():
  def __init__(self, protocol_file_path):
    pass

  def encode(self, which, address):
    if (which in self.proto.keys()):
      encoded = self.proto[which]["encode"]
      if address in self.proto[which]["address"]:
        encoded += self.proto[which]["address"][address]
        encoded += '\n'
        return encoded.encode('utf-8')
    
    return encoded
