import sys, io
from PySide2.QtWidgets import QApplication
import queue
from source.utilities import cli, logger
from source.ui import uiBase, uiImu, uiControl, uiDebug
from source.comms import commsClient
import json

class UiExecute:
  def __init__(self, settings_file_path, ui_file_path):
    setting_file = open(settings_file_path, "r")
    settings = json.load(setting_file)
    setting_file.close()
    args = cli.get_args(settings["default"])
  
    if args.no_connect == True:
      from source.sockets import socketFake
      ClientSocket = socketFake.SocketFake
      serverAddress = ''
      port = 0
    elif args.tcp != None:
      from source.sockets import socketTcp
      ClientSocket = socketTcp.SocketTcp
      serverAddress = args.tcp[0]
      port = int(args.tcp[1])
    else:
      from source.sockets import socketBt
      ClientSocket = socketBt.SocketBt
      serverAddress = args.bluetooth[0]
      port = args.bluetooth[1]

    if args.data_logging != None:
      log_entries = logger.LogEntries()
    else:
      log_entries = None
      log_file = None
      log = None

    app = QApplication(sys.argv)

    window = uiBase.load_from_file(ui_file_path)

    command_queue = queue.Queue()
    client_socket = ClientSocket(serverAddress, port)
    comms = commsClient.CommsClient(client_socket, command_queue)
    window.add_upkeep(20, comms.upkeep)
    window.set_command_queue(command_queue)

    window.load_ui_elements([uiImu, uiControl, uiDebug], comms, log_entries)

    if log_entries != None:
      log_file = open(args.data_logging, "w+")
      log = logger.Logger(log_file, log_entries)
      window.add_upkeep(100, log.publish)

    sys.exit(app.exec_())

    log_file.close()
