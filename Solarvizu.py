import PyQt5
import pyqtgraph as pg
import numpy as np

# --------------------------------- Graphical Settings ------------------------------------------------------

pg.setConfigOption('background', 'w')
pen = pg.mkPen(color=(255, 0, 0), width=5, style=QtCore.Qt.DashLine)

# --------------------------------- Parameters Settings ---------------------------------------------------------

length = 1.5 # in meters
width = 0.7 # in meters

angle_1 = 20.*np.pi/180. # in degrees [0, 360]
angle_2 = 0.*np.pi/180. # in degrees [0, 360]

boundary_length = 2 # in meters
boundary_width = 1.5 # in meters
boundary_angle = 360 # in degrees

x = np.array([0., np.cos(angle_1)*length])
y = np.array([0., np.sin(angle_1)*length])

plotWidget_1 = pg.plot(title="Side_View")
plotWidget_1.plot(x, y, pen=pen, name="side_view")

x0 = np.array([0., np.sin(angle_1)*length])

plotWidget_2 = pg.plot(title="Sky_View")
plotWidget_2.plot(x0, fillLevel=np.cos(angle_1)*length, name="sky_view")

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()