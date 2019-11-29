# Author: Hoani
#
# Manual control GUI
from pyGuiComms.ui import uiExecute

if __name__ == '__main__':
  gui = uiExecute.UiExecute("ui/ManualControl.ui", "json/settings.json", "json/widgets.json")
