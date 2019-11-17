import sys, io
from PySide2.QtWidgets import QApplication
import queue
from source.utilities import cli
from source.ui import uiBase, uiImu, uiControl, uiDebug
from source.comms import commsClient

if __name__ == '__main__':

  args = cli.get_args()

  useTcp = True
  
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
    

  app = QApplication(sys.argv)

  window = uiBase.load_from_file('ui/ManualControl.ui')

  command_queue = queue.Queue()
  client_socket = ClientSocket(serverAddress, port)
  comms = commsClient.CommsClient(client_socket, command_queue)
  window.add_upkeep(20, comms.upkeep)
  window.set_command_queue(command_queue)

  window.load_ui_elements(comms, [uiImu, uiControl, uiDebug])

  sys.exit(app.exec_())



  

