from PySide2.QtWidgets import QSizePolicy
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as pyplot
import vect




class PlotCanvas(FigureCanvas):

  def __init__(self, data, title= None, parent=None, width=5, height=4, dpi=100):
    fig = matplotlib.figure.Figure(figsize=(width, height), dpi=dpi)
    fig.set_facecolor('#00000000')
    
    self.data = vect.Vec3([], [], [])

    FigureCanvas.__init__(self, fig)
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self,
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

    self.subplot = self.figure.add_subplot(111)    

    if (title != None):
      title_color = '#FFFFFF'
      self.subplot.set_title(title, color=title_color)
    self.l1,self.l2,self.l3, = self.subplot.plot(self.data.x, 'r', self.data.y, 'b', self.data.z, 'g')
    self.index = 0
    self._set_style()
    self.draw()

  def _set_style(self):
    axis_color = '#FFFFFF'
    grid_color = '#025d5e'
    face_color = '#014d4e'

    self.subplot.spines['bottom'].set_color(axis_color)
    self.subplot.spines['top'].set_color(axis_color)
    self.subplot.spines['left'].set_color(axis_color)
    self.subplot.spines['right'].set_color(axis_color)
    self.subplot.tick_params(axis='both', colors=axis_color, which='both')

    self.subplot.grid(True, which='both', color=grid_color)

    self.subplot.set_facecolor(face_color)

  def update_data(self, new_data):
    low = max(0,min(1, self.index - 100))
    high = min(self.index, 101)
    self.l1.set_xdata(np.append(self.l1.get_xdata(), self.index/10.0)[low:high])
    self.l2.set_xdata(np.append(self.l2.get_xdata(), self.index/10.0)[low:high])
    self.l3.set_xdata(np.append(self.l3.get_xdata(), self.index/10.0)[low:high])
    self.l1.set_ydata(np.append(self.l1.get_ydata(), new_data.x)[low:high])
    self.l2.set_ydata(np.append(self.l2.get_ydata(), new_data.y)[low:high])
    self.l3.set_ydata(np.append(self.l3.get_ydata(), new_data.z)[low:high])
    self.index += 1
    self.subplot.relim()
    self.subplot.autoscale_view()
    self.draw()