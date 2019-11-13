import sys, io
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2 import QtCore, QtWidgets
import extraConsole
import threading
import queue
import clientThread
import vect
import baseUi





if __name__ == '__main__':
  echo = True
  serverMACAddress = '38:D2:69:E1:11:CB'
  port = 3
  if echo == True:
    import echoClient
    ClientSocket = echoClient.EchoClient
  else:
    import btClient
    ClientSocket = btClient.BtClient
    
  
  client_socket = ClientSocket(serverMACAddress, port)

  app = QApplication(sys.argv)
  #ui_file = QFile('BasicCommands.ui')
  ui_file = QFile('ManualControl.ui')
  ui_file.open(QFile.ReadOnly)

  loader = QUiLoader()
  loader.registerCustomWidget(baseUi.MainWindow)
  window = loader.load(ui_file)
  window.init_signals()
  window.register_client(client_socket) 

  ui_file.close()

  sys.exit(app.exec_())



  

