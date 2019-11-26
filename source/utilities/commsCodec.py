
import json

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
      encoded += self.protocol["separator"]
      types = extract_types(root, path[1:])
      print(types)
      if types[0] == "u8":
        encoded += "{:02x}".format(packet.payload[0])
      elif types[0] == "u16":
        encoded += "{:04x}".format(packet.payload[0])
      else:
        encoded += "{:08x}".format(packet.payload[0])

    encoded += self.protocol["end"]
    return encoded.encode('utf-8')

