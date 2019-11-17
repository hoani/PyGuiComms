import argparse

def get_args():
  parser = argparse.ArgumentParser(description='A robot GUI')
  parser.add_argument(
    '--bluetooth', 
    help="Add host bluetooth port, requires MAC address and port number",
    default=['38:D2:69:E1:11:CB', 3],
    metavar=("MAC","port"),
    nargs=2,
    type=str
    )
  parser.add_argument(
    '--tcp', 
    help="Add host tcp port, requires ip address and port number",
    default=None,
    metavar=("ip", "port"),
    nargs=2,
    type=str
    )

  parser.add_argument(
    '--no-connect', 
    help="Run in no-connect mode", 
    action='store_true'
    )

  args = parser.parse_args()

  return args