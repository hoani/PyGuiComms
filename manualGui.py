import sys, io
from PySide2.QtWidgets import QApplication
import queue
import source.utilities.vect
from source.ui import uiBase, uiImu, uiControl, uiDebug
from source.comms import commsClient

if __name__ == '__main__':

  echo = False
  serverMACAddress = '38:D2:69:E1:11:CB'
  port = 3
  if echo == True:
    from source.sockets import socketFake
    ClientSocket = socketFake.SocketFake
  else:
    from source.sockets import socketBt
    ClientSocket = socketBt.SocketBt
    

  app = QApplication(sys.argv)

  window = uiBase.load_from_file('ui/ManualControl.ui')

  command_queue = queue.Queue()
  client_socket = ClientSocket(serverMACAddress, port)
  comms = commsClient.CommsClient(client_socket, command_queue)
  window.add_upkeep(20, comms.upkeep)
  window.set_command_queue(command_queue)

  uiBase.load_ui_elements(window, comms, [uiImu, uiControl, uiDebug])

  sys.exit(app.exec_())



  

