
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
    encoded = self.protocol["category"][packet.category]["encode"]
    if packet.path != None:
      path = packet.path.split("/")
      root = self.protocol["data"][path[0]]
      address = int(root["_addr"])
      if len(path) > 1:
        address += count_to_path(root, path[1:])
      encoded += "{:04x}".format(address)
    if packet.payload != None:
      encoded += ",a5"
    encoded += self.protocol["end"]["encode"]
    return encoded.encode('utf-8')

