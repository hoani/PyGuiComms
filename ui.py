import sys, io
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtWidgets
import vect
import baseUi
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
    
  client_socket = ClientSocket(serverMACAddress, port)
  comms = commsClient.CommsClient(client_socket)

  app = QApplication(sys.argv)
  ui_file = QFile('ManualControl.ui')
  ui_file.open(QFile.ReadOnly)

  loader = QUiLoader()
  loader.registerCustomWidget(baseUi.MainWindow)
  window = loader.load(ui_file)
  
  window.set_subscriptions(comms.subscribe)
  window.add_upkeep(20, comms.upkeep)

  ui_file.close()

  sys.exit(app.exec_())



  

