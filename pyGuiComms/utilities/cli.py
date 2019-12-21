import argparse
from datetime import datetime

def get_args(default_settings):

  parser = argparse.ArgumentParser(description='A robot GUI')
  parser.add_argument(
    '--bluetooth',
    help="Add host bluetooth port, requires MAC address and port number",
    default=[default_settings["bluetooth"]["address"], default_settings["bluetooth"]["port"]],
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
    '--tcp-remote-log',
    help="Add remote logging tcp port",
    default=None,
    metavar="port"
  )

  parser.add_argument(
    '--no-connect',
    help="Run in no-connect mode",
    action='store_true',
    )

  parser.add_argument(
    '--data-logging',
    help="Enable data logging as a csv for analysis",
    action="store_const",
    default=None,
    const = datetime.now().strftime("%Y%m%d-%H%M%S_log.csv")
  )

  parser.add_argument(
    '--event-logging',
    help="Enable event logging - logs all stdout",
    action="store_const",
    default=None,
    const = datetime.now().strftime("%Y%m%d-%H%M%S_event.txt")
  )

  args = parser.parse_args()

  return args

if __name__ == "__main__":
  print("Args:")
  print(get_args())