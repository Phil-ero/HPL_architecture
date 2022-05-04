from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow)
import pyqtgraph as pg
import numpy as np
import sys

# -------------------- CLASS QWIDGET ------------------------------------

class Solar_Panel(QWidget):
    def __init__(self, length, width, angle_1, angle_2):
        super().__init__()
        self.init_data(length, width, angle_1, angle_2)

    def init_data(self, length, width, angle_1, angle_2):
        boundary_length = 2 # [m]
        boundary_width = 1.5 # [m]

        x1 = np.array([0, np.cos(angle_1*np.pi/180)*length])
        y1 = np.array([0, np.sin(angle_1*np.pi/180)*length])
        data_1 = np.array([x1, y1])

        x2 = np.array([0., width])
        y2 = np.array([np.cos(angle_1*np.pi/180)*length, np.cos(angle_1*np.pi/180)*length])
        data_2 = np.array([x2, y2])

        point = np.array([width/2, 0.05+np.cos(angle_1*np.pi/180)*length*0.5])
        angles = np.array([angle_1, angle_2])

        self.initUI(data_1, data_2, point, angles)
    
    def initUI(self, data_1, data_2, point, angles):
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)
        pen_gen = pg.mkPen(color=(51, 153, 255), width=5)

        widget_1 = pg.PlotWidget(name = 'Side View')
        widget_1.plot(title="Side_View")
        widget_1.showGrid(x = True, y = True)
        widget_1.setLabel('bottom', "Length")
        widget_1.setLabel('left', "Height")
        text = pg.TextItem(text = str(angles[0]), anchor = (0,0))
        widget_1.addItem(text)
        widget_1.plot(data_1[0], data_1[1], pen=pen_gen, name="side_view")
        widget_1.setXRange(0, data_1[0][1])
        widget_1.setYRange(0, data_1[1][1])

        widget_2 = pg.PlotWidget(name = 'Sky View')
        widget_2.plot(title="Sky_View")
        widget_2.showGrid(x = True, y = True)
        widget_2.setLabel('bottom', "Width")
        widget_2.setLabel('left', "Length")
        widget_2.plot(data_2[1], fillLevel=0.0, brush=(50,50,200,100), name="sky_view")
        arrow = pg.ArrowItem(angle = 90+angles[1], headLen = 50, pos = point)
        widget_2.addItem(arrow)
        widget_2.setXRange(0, data_2[0][1])
        widget_2.setYRange(0, data_2[1][1])

        hbox.addWidget(widget_1)
        hbox.addWidget(widget_2)

        self.setLayout(hbox)
        self.setGeometry(400, 300, 400, 300)

# --------------------------------- Graphical Settings ------------------------------------------------------
length_ini = 1.5 # [m]
width_ini = 0.7 # [m]
angle_1_ini = 20. # degrees
angle_2_ini = 45. # degrees

def test():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Solar Panel test window")
    win.setCentralWidget(Solar_Panel(length_ini, width_ini, angle_1_ini, angle_2_ini))
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test()