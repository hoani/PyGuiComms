import sys, io
from PySide2.QtWidgets import QApplication
import queue
from pyGuiComms.utilities import cli, logger
from pyGuiComms.ui import uiBase, uiImu, uiControl, uiDebug
from pyGuiComms.comms import commsClient
import json


class UiExecute:
  def __init__(self, ui_file_path, settings_file_path, widgets_file_path):
    with open(settings_file_path, "r") as settings_file:
      settings = json.load(settings_file)
    
    with open(widgets_file_path, "r") as widgets_file:
      widget_settings = json.load(widgets_file)

    
    args = cli.get_args(settings["default"])
  
    if args.no_connect == True:
      from pyGuiComms.sockets import socketFake
      ClientSocket = socketFake.SocketFake
      serverAddress = ''
      port = 0
    elif args.tcp != None:
      from pyGuiComms.sockets import socketTcp
      ClientSocket = socketTcp.SocketTcp
      serverAddress = args.tcp[0]
      port = int(args.tcp[1])
    else:
      from pyGuiComms.sockets import socketBt
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

    window.load_ui_elements([uiImu, uiControl, uiDebug], comms, log_entries, widget_settings)



    if log_entries != None:
      log_file = open(args.data_logging, "w+")
      log = logger.Logger(log_file, log_entries)
      window.add_upkeep(100, log.publish)

    sys.exit(app.exec_())

    log_file.close()
