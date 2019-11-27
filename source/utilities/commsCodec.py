
import json, struct

def count_depth(root):
  count = 0
  if "type" in root.keys():
    return 0

  for key in root.keys():
    if key[0] != "_":
      count += 1
      count += count_depth(root[key])

  return count


def count_to_path(root, path):
  count = 0
  if path == None:
    return count_depth(root)
  
  search = path[0]
  if search in root.keys():
    for key in root.keys():
      if key[0] != "_":
        count += 1
        if key != search:
          if "type" in root[key]:
            pass
          else:
            count += count_depth(root[key])
        else:
          break
    
    if len(path) > 1:
      incr = count_to_path(root[search], path[1:])
      if (incr != None):
        count += incr
      else:
        return None

  else:
    return None

  return count

def get_struct(root, path):
  if path == []:
    return root

  if path[0] in root.keys():
    if len(path) == 1:
      return root[path[0]]
    else:
      return get_struct(root[path[0]], path[1:])
  else:
    return None

def extract_types(root, path):
  start = get_struct(root, path)
  types = []
  if start != None:
    if "type" in start.keys():
      types.append(start["type"])
    else:
      for key in start.keys():
        if key[0] != "_":
          types = types + extract_types(start[key], [])

  return types

def clamp(value, min_value, max_value):
  return max(min_value, min(value, max_value))
  
def encode_types(item, typeof):
  if typeof == "u8":
    return "{:02x}".format(clamp(item, 0x00, 0xff))
  elif typeof == "u16":
    return "{:04x}".format(clamp(item, 0x0000, 0xffff))
  elif typeof == "u32":
    return "{:08x}".format(clamp(item, 0x00000000, 0xffffffff))
  elif typeof == "u64":
    return "{:016x}".format(clamp(item, 0x0000000000000000, 0xffffffffffffffff))
  if typeof == "i8":
    return "{:02x}".format(item + 0x100 if item < 0 else item)
  elif typeof == "i16":
    return "{:04x}".format(item + 0x10000 if item < 0 else item)
  elif typeof == "i32":
    return "{:08x}".format(item + 0x100000000 if item < 0 else item)
  elif typeof == "i64":
    return "{:016x}".format(item + 0x10000000000000000 if item < 0 else item)
  elif typeof == "string":
    return item
  elif typeof == "bool":
    return "1" if item == True else "0"
  elif typeof == "float":
    return ''.join(format(x, '02x') for x in struct.pack('>f', item))
  elif typeof == "double":
    return ''.join(format(x, '02x') for x in struct.pack('>d', item))
  else:
    return ""

class Packet():
  def __init__(self, category, path=None, payload=None):
    self.category = category
    self.path = path
    self.payload = payload

class Codec():
  def __init__(self, protocol_file_path):
    with open(protocol_file_path, "r") as protocol_file:
      self.protocol = json.load(protocol_file)

  def encode(self, packet):
    encoded = self.protocol["category"][packet.category]
    if packet.path != None:
      path = packet.path.split("/")
      root = self.protocol["data"][path[0]]
      address = int(root["_addr"], 16)
      if len(path) > 1:
        address += count_to_path(root, path[1:])
      encoded += "{:04x}".format(address)
    if packet.payload != None:
      types = extract_types(root, path[1:])
      count = min(len(types), len(packet.payload))
      for i in range(count):
        encoded += self.protocol["separator"]
        encoded += encode_types(packet.payload[i], types[i])

    encoded += self.protocol["end"]
    return encoded.encode('utf-8')

