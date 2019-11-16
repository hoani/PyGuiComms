import sys, io
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtWidgets
import queue
import vect
import baseUi, imuUi, controlUi, debugUi
import commsClient

if __name__ == '__main__':
  echo = False
  serverMACAddress = '38:D2:69:E1:11:CB'
  port = 3
  if echo == True:
    import echoClient
    ClientSocket = echoClient.EchoClient
  else:
    import btClient
    ClientSocket = btClient.BtClient
    
  command_queue = queue.Queue()

  client_socket = ClientSocket(serverMACAddress, port)
  comms = commsClient.CommsClient(client_socket, command_queue)

  app = QApplication(sys.argv)
  ui_file = QFile('ManualControl.ui')
  ui_file.open(QFile.ReadOnly)

  loader = QUiLoader()
  loader.registerCustomWidget(baseUi.MainWindow)
  window = loader.load(ui_file)
  window.set_command_queue(command_queue)
  window.add_upkeep(20, comms.upkeep)

  ui_imu = imuUi.ImuUi(window)
  ui_imu.set_subscriptions(comms.subscribe)

  ui_control = controlUi.ControlUi(window)
  ui_control.set_subscriptions(comms.subscribe)

  ui_debug = debugUi.DebugUi(window)
  ui_debug.set_subscriptions(comms.subscribe)

  ui_file.close()

  sys.exit(app.exec_())



  

