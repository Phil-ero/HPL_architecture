import sys
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,\
    QApplication, QMainWindow, QSlider, QLineEdit, QGridLayout, QLabel,\
    QLayout, QSizePolicy, QDial
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import numpy as np

# -------------------- CLASS QWIDGET ------------------------------------

class Solar_Panel(QWidget):
    def __init__(self, angle_1 : int, angle_2 : int, length : int, _width : int):
        super().__init__()

        self.angle_1 = angle_1
        self.angle_2 = angle_2
        self.length = length
        self._width = _width

        layout = QHBoxLayout(self)

        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)

        self.widget_1 = pg.PlotWidget(name = 'Side View')
        self.widget_1.getPlotItem().enableAutoRange()
        self.widget_1.setMouseEnabled(x=False,y=False)
        self.widget_1.plot([0., np.cos(self.angle_1*np.pi/180)*self.length], [0., np.sin(self.angle_1*np.pi/180)*self.length], pen = pg.mkPen(color='b', width = 5.))
        self.widget_1.showGrid(x = True, y = True)
        self.widget_1.setTitle('Angle 1: ' + str(self.angle_1) + '°')
        self.widget_1.setLabel('bottom', "Length")
        self.widget_1.setLabel('left', "Height")
        self.widget_1.setMinimumWidth(200)
        self.widget_1.setMinimumHeight(200)
        self.widget_1.autoRange()

        #self.widget_1.signal.connect(self.slot_function_side)

        self.widget_2 = pg.PlotWidget(name = 'Sky View')
        self.widget_2.getPlotItem().enableAutoRange()
        self.widget_2.setMouseEnabled(x=False,y=False)
        self.widget_2.plot([0., self._width], [np.cos(self.angle_1*np.pi/180)*self.length, np.cos(self.angle_1*np.pi/180)*self.length], fillLevel=0., fillBrush=(50,50,200,100), title="Sky_View")
        self.widget_2.showGrid(x = True, y = True)
        self.widget_2.setTitle('Angle 2: ' + str(self.angle_2) + '°')
        self.widget_2.setLabel('bottom', "Width")
        self.widget_2.setLabel('left', "Length")
        self.widget_2.setMinimumWidth(200)
        self.widget_2.setMinimumHeight(200)
        self.widget_2.autoRange()

        self.point = np.array([self._width/2, np.cos(self.angle_1*np.pi/180)*self.length*0.5])
        self.arrow = pg.ArrowItem(headLen = 20, tailLen = 35, tailWidth = 5, pen =  pg.mkPen(color='w', width = 0.), brush= pg.mkBrush(color = 'w'), angle = -90 - self.angle_2, pos = self.point)
        self.arrow_sud = pg.ArrowItem(headLen = 20, tailLen = 35, tailWidth = 5, pen =  pg.mkPen(color='r', width = 0.), brush= pg.mkBrush(color = 'r'), angle = -90, pos = self.point)
        self.widget_2.addItem(self.arrow)
        self.widget_2.addItem(self.arrow_sud)

        #self.widget_2.signal.connect(self.slot_function_sky)

        layout.addWidget(self.widget_1)
        #layout.addWidget(QLabel(str(self.angle_1)),0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.widget_2)


    #def slot_function_side(self):


    #def slot_function_sky(self):
# --------------------------------- Graphical Settings ------------------------------------------------------

def test():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Solar Panel test window")
    win.setCentralWidget(Solar_Panel(20, 45, 150, 70))
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test()