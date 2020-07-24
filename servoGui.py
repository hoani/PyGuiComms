# Author: Hoani
#
# Manual Servo Control UI
from pyGuiComms.ui import uiExecute

if __name__ == '__main__':
    gui = uiExecute.UiExecute(
      "ui/Servo.ui",
      "config/settings.json",
      "config/widgets.json",
      "config/protocol.json"
    )
