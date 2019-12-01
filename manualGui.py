# Author: Hoani
#
# Manual control GUI
from pyGuiComms.ui import uiExecute
import sys

if __name__ == '__main__':
  sys.path.insert(0,'./external/RoBus/RoBus')
  gui = uiExecute.UiExecute("ui/ManualControl.ui", "config/settings.json", "config/widgets.json", "config/protocol.json")
