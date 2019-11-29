# Author: Hoani
#
# Allows real time plotting using QT pyside

from PySide2.QtWidgets import QSizePolicy
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as pyplot
from pyGuiComms.utilities import vect



class PlotCanvas(FigureCanvas):
  def __init__(self, lines, max_data_points = 100, title= None, parent=None, width=5, height=4, dpi=100):
    fig = matplotlib.figure.Figure(figsize=(width, height), dpi=dpi)
    fig.set_facecolor('#00000000')

    FigureCanvas.__init__(self, fig)
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self,
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

    self.subplot = self.figure.add_subplot(111)    

    if (title != None):
      title_color = '#CCCCCC'
      self.subplot.set_title(title, color=title_color)

    self.lines = []
    for i in range(len(lines)):
      line = self.subplot.plot(0, 0, lines[i])[0]
      self.lines.append(line)
    
    self.index = 0
    self.max_data_points = max_data_points
    self._set_style()
    self.draw()

  def _set_style(self):
    axis_color = '#CCCCCC'
    grid_color = '#025d5e'
    face_color = '#014d4e'

    self.subplot.spines['bottom'].set_color(axis_color)
    self.subplot.spines['top'].set_color(axis_color)
    self.subplot.spines['left'].set_color(axis_color)
    self.subplot.spines['right'].set_color(axis_color)
    self.subplot.tick_params(axis='both', colors=axis_color, which='both')

    self.subplot.grid(True, which='both', color=grid_color)

    self.subplot.set_facecolor(face_color)

  def update_data(self, t, new_data):
    low = max(0,min(1, self.index - self.max_data_points))
    high = min(self.index, self.max_data_points + 1)

    for i in range(len(self.lines)):
      self.lines[i].set_xdata(np.append(self.lines[i].get_xdata(), t)[low:high])
      self.lines[i].set_ydata(np.append(self.lines[i].get_ydata(), new_data[i])[low:high])

    self.index += 1
    self.subplot.relim()
    self.subplot.autoscale_view()
    self.draw()



class XyzPlotCanvas(PlotCanvas):
  def __init__(self, max_data_points = 100, title = None, parent = None, width = 5, height = 4, dpi = 100 ):
    super().__init__(['r','b','g'], max_data_points, title, parent, width, height, dpi)

  def update_data(self, t, data):
    data_array = [data.x, data.y, data.z]

    super().update_data(t, data_array)