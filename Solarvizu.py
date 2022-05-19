import sys
import pyqtgraph as pg
import numpy as np
import typing
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,\
    QApplication, QMainWindow, QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

# -------------------- CLASS QWIDGET ------------------------------------

class Solar_Panel(QWidget):
    def __init__(self, inclination_angle: int, orientation_angle: int, length: int, _width: int):
        super().__init__()

        self._inclination_angle = inclination_angle
        self._orientation_angle = orientation_angle
        self._length = length
        self._width = _width
        self._halfdiag = np.sqrt(self._length**2 + self._width**2)/2

        layout = QHBoxLayout(self)

        #Widget Side View

        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)

        self.side_widget = pg.PlotWidget(name='Side View')
        self.side_widget.getPlotItem().getViewBox().setLimits(
            xMin=-10, xMax=self._length + 10, yMin=-10, yMax=self._length + 10)
        self.side_widget.setMouseEnabled(x=False, y=False)
        self.side_widget.setXRange(0,self._length)
        self.side_widget.setYRange(0,self._length)
        self.side_plot: pg.PlotDataItem = self.side_widget.plot(
            [0., np.cos(self._inclination_angle*np.pi/180)*self._length],
            [0., np.sin(self._inclination_angle*np.pi/180)*self._length],
            pen=pg.mkPen(color = 'b', width=4.))

        self.side_widget.showGrid(x=True, y=True)
        self.side_widget.setTitle(
            'Inclination: ' + str(self._inclination_angle) + '°')
        self.side_widget.setLabel('bottom', "Length")
        self.side_widget.setLabel('left', "Height")
        #self.side_widget.setMinimumWidth(200)
        #self.side_widget.setMinimumHeight(200)

        #Widget Top View

        self.top_widget = pg.PlotWidget(name='Top View')
        self.top_widget.setXRange(-self._halfdiag,self._halfdiag)
        self.top_widget.setYRange(-self._halfdiag,self._halfdiag)
        self.top_widget.setMouseEnabled(x=False, y=False)
        self.top_widget.showGrid(x=True, y=True)
        self.top_widget.setTitle(
           'Orientation: ' + str(self._orientation_angle) + '°')
        self.top_widget.setLabel('bottom', "Width")
        self.top_widget.setLabel('left', "Length")
        #self.top_widget.setMinimumWidth(200)
        #self.top_widget.setMinimumHeight(200)

        #Rotation of Top view and Curve

        p1 = np.array([-1*self._width/2, -1*np.cos(self._inclination_angle*np.pi/180)*self._length/2])
        p2 = np.array([-1*self._width/2, np.cos(self._inclination_angle*np.pi/180)*self._length/2])
        p3 = np.array([self._width/2, np.cos(self._inclination_angle*np.pi/180)*self._length/2])
        p4 = np.array([self._width/2, -1*np.cos(self._inclination_angle*np.pi/180)*self._length/2])

        b1 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p1[0] - np.sin(-self._orientation_angle*np.pi/180)*p1[1], np.sin(-self._orientation_angle*np.pi/180)*p1[0] + np.cos(-self._orientation_angle*np.pi/180)*p1[1]])
        b2 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p2[0] - np.sin(-self._orientation_angle*np.pi/180)*p2[1], np.sin(-self._orientation_angle*np.pi/180)*p2[0] + np.cos(-self._orientation_angle*np.pi/180)*p2[1]])
        b3 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p3[0] - np.sin(-self._orientation_angle*np.pi/180)*p3[1], np.sin(-self._orientation_angle*np.pi/180)*p3[0] + np.cos(-self._orientation_angle*np.pi/180)*p3[1]])
        b4 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p4[0] - np.sin(-self._orientation_angle*np.pi/180)*p4[1], np.sin(-self._orientation_angle*np.pi/180)*p4[0] + np.cos(-self._orientation_angle*np.pi/180)*p4[1]])
        
        x_tot = np.array([b1[0], b2[0], b3[0], b4[0], b1[0]])
        y_tot = np.array([b1[1], b2[1], b3[1], b4[1], b1[1]])

        self.curve: pg.PlotDataItem = pg.PlotCurveItem()
        self.curve.setData(x_tot, y_tot, fillLevel = 1., brush = pg.mkBrush(color = (0,181,226,100)))
        self.top_widget.addItem(self.curve)
        
        #Arrow in Top View

        self.__arrow_headLen = 20
        self.__arrow_tailLen = 20
        self.__arrow_angle = 90 + self._orientation_angle # 0° is looking left, 90° is looking up
        self.__arrow_pos = [0.0, 0.0]
        self.arrow: pg.ArrowItem = pg.ArrowItem(headLen=self.__arrow_headLen, tailLen=self.__arrow_tailLen, tailWidth=5, pen=pg.mkPen(
           color='b', width=0.), brush=pg.mkBrush(color='b'), angle=self.__arrow_angle, pos=self.__arrow_pos)
        self.arrow_north: pg.ArrowItem = pg.ArrowItem(headLen=20, tailLen=35, tailWidth=5, pen=pg.mkPen(
           color='r', width=0.), brush=pg.mkBrush(color='r'), angle=90, pos=[self._length/2, self._length/2])
        self.top_widget.addItem(self.arrow)
        self.top_widget.addItem(self.arrow_north)

        layout.addWidget(self.side_widget)
        layout.addWidget(QLabel(str(self._inclination_angle)),0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.top_widget)
        
        self._replot()

    def _replot(self) -> None:

        self._halfdiag = np.sqrt(self._length**2 + self._width**2)
        #Update Side

        self.side_plot.setData([0., np.cos(self._inclination_angle*np.pi/180)*self._length], [0., np.sin(self._inclination_angle*np.pi/180)*self._length])
        self.side_widget.setTitle('Side View -- Inclination: ' + str(self._inclination_angle) + '°')
        self.side_widget.getPlotItem().getViewBox().setLimits(xMin=-10, xMax=self._length + 10, yMin=-10, yMax=self._length + 10)
        self.side_widget.setXRange(0,self._length)
        self.side_widget.setYRange(0,self._length)
        #Update Rotation

        p1 = np.array([-1*self._width/2, -1*np.cos(self._inclination_angle*np.pi/180)*self._length/2])
        p2 = np.array([-1*self._width/2, np.cos(self._inclination_angle*np.pi/180)*self._length/2])
        p3 = np.array([self._width/2, np.cos(self._inclination_angle*np.pi/180)*self._length/2])
        p4 = np.array([self._width/2, -1*np.cos(self._inclination_angle*np.pi/180)*self._length/2])

        b1 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p1[0] - np.sin(-self._orientation_angle*np.pi/180)*p1[1], np.sin(-self._orientation_angle*np.pi/180)*p1[0] + np.cos(-self._orientation_angle*np.pi/180)*p1[1]])
        b2 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p2[0] - np.sin(-self._orientation_angle*np.pi/180)*p2[1], np.sin(-self._orientation_angle*np.pi/180)*p2[0] + np.cos(-self._orientation_angle*np.pi/180)*p2[1]])
        b3 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p3[0] - np.sin(-self._orientation_angle*np.pi/180)*p3[1], np.sin(-self._orientation_angle*np.pi/180)*p3[0] + np.cos(-self._orientation_angle*np.pi/180)*p3[1]])
        b4 = np.array([np.cos(-self._orientation_angle*np.pi/180)*p4[0] - np.sin(-self._orientation_angle*np.pi/180)*p4[1], np.sin(-self._orientation_angle*np.pi/180)*p4[0] + np.cos(-self._orientation_angle*np.pi/180)*p4[1]])
        
        x_tot = np.array([b1[0], b2[0], b3[0], b4[0], b1[0]])
        y_tot = np.array([b1[1], b2[1], b3[1], b4[1], b1[1]])

        #Update Top

        self.curve.setData(x_tot, y_tot)
        self.top_widget.setTitle('Top View -- Orientation: ' + str(self._orientation_angle) + '°')
        
        self.top_widget.setXRange(-self._halfdiag,self._halfdiag)
        self.top_widget.setYRange(-self._halfdiag,self._halfdiag)
        
        self.__arrow_angle = 90 + self._orientation_angle
        self.arrow.setStyle(angle=self.__arrow_angle)
        
        self.arrow_north.setPos(self._halfdiag*2/3, self._halfdiag*2/3)

        return

    def update_inclination_angle(self, a1: int) -> None:
        self._inclination_angle = a1
        self._replot()
        return

    def update_orientation_angle(self, a2: int) -> None:
        self._orientation_angle = a2
        self._replot()
        return
    
    def update_panel_length(self, l:int) -> None:
        self._length = l
        self._replot()
        return
    
    def update_panel_width(self, w:int) -> None:
        self._width = w
        self._replot()
        return

def test():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Solar Panel test window")
    win.setCentralWidget(Solar_Panel(40, 40, 200, 50))
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
