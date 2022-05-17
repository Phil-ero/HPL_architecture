import sys
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,\
    QApplication, QMainWindow, QSlider, QLineEdit, QGridLayout, QLabel,\
    QLayout, QSizePolicy, QDial
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import numpy as np
import typing

# -------------------- CLASS QWIDGET ------------------------------------


class Solar_Panel(QWidget):
    def __init__(self, inclination_angle: int, orientation_angle: int, length: int, _width: int):
        super().__init__()

        self._inclination_angle = inclination_angle
        self._orientation_angle = orientation_angle
        self._length = length
        self._width = _width

        layout = QHBoxLayout(self)

        pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True)

        self.side_widget = pg.PlotWidget(name='Side View')
        self.side_widget.getPlotItem().getViewBox().setLimits(
            xMin=-10, xMax=self._length + 10, yMin=-10, yMax=self._length + 10)
        self.side_widget.setXRange(0, self._length, 1)
        self.side_widget.setYRange(0, self._length, 1)
        self.side_widget.setMouseEnabled(x=False, y=False)
        self.side_plot: pg.PlotDataItem = self.side_widget.plot(
            [0., np.cos(self._inclination_angle*np.pi/180)*self._length],
            [0., np.sin(self._inclination_angle*np.pi/180)*self._length],
            pen=pg.mkPen(color='b', width=5.))

        self.side_widget.showGrid(x=True, y=True)
        self.side_widget.setTitle(
            'Inclination: ' + str(self._inclination_angle) + '°')
        self.side_widget.setLabel('bottom', "Length")
        self.side_widget.setLabel('left', "Height")
        self.side_widget.setMinimumWidth(200)
        self.side_widget.setMinimumHeight(200)

        # self.side_widget.signal.connect(self.slot_function_side)

        self.top_widget = pg.PlotWidget(name='Top View')
        self.top_widget.getPlotItem().getViewBox().setLimits(
            xMin=-10, xMax=self._width + 30, yMin=-10, yMax=self._length + 30)
        self.top_widget.setXRange(0, self._width, 1)
        self.top_widget.setYRange(0, self._length, 1)
        self.top_widget.setMouseEnabled(x=False, y=False)
        self.top_plot: pg.PlotDataItem = self.top_widget.plot([0., self._width], [np.cos(self._inclination_angle*np.pi/180)*self._length, np.cos(
            self._inclination_angle*np.pi/180)*self._length], fillLevel=0., fillBrush=(50, 50, 200, 100), title="Sky_View")
        self.top_widget.showGrid(x=True, y=True)
        self.top_widget.setTitle(
            'Orientation: ' + str(self._orientation_angle) + '°')
        self.top_widget.setLabel('bottom', "Width")
        self.top_widget.setLabel('left', "Length")
        self.top_widget.setMinimumWidth(200)
        self.top_widget.setMinimumHeight(200)
        self.top_widget.autoRange()

        self.__arrow_headLen = 20
        self.__arrow_tailLen = 20
        self.__arrow_angle = 90 + self._orientation_angle # 0° is looking left, 90° is looking up
        
        # In the function, provide the arrow's tip position, not its base
        self.__arrow_pos = [
            self._width/2, np.cos(self._inclination_angle*np.pi/180)*self._length*0.5]
        
        self.arrow: pg.ArrowItem = pg.ArrowItem(headLen=self.__arrow_headLen, tailLen=self.__arrow_tailLen, tailWidth=5, pen=pg.mkPen(
            color='w', width=0.), brush=pg.mkBrush(color='w'), angle=self.__arrow_angle, pos=self.__arrow_pos)
        self.arrow_north: pg.ArrowItem = pg.ArrowItem(headLen=20, tailLen=35, tailWidth=5, pen=pg.mkPen(
            color='r', width=0.), brush=pg.mkBrush(color='r'), angle=90, pos=[self._width*+15, self._length + 15])
        self.top_widget.addItem(self.arrow)
        self.top_widget.addItem(self.arrow_north)

        # self.top_widget.signal.connect(self.slot_function_sky)

        layout.addWidget(self.side_widget)
        #layout.addWidget(QLabel(str(self.inclination_angle)),0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.top_widget)
        
        self._replot()

    def _replot(self) -> None:
        self.side_plot.setData([0., np.cos(self._inclination_angle*np.pi/180)*self._length], [0., np.sin(
            self._inclination_angle*np.pi/180)*self._length])
        self.side_widget.setTitle(
            'Side View -- Inclination: ' + str(self._inclination_angle) + '°')
        self.side_widget.getPlotItem().getViewBox().setLimits(
            xMin=-10, xMax=self._length + 10, yMin=-10, yMax=self._length + 10)
        self.side_widget.setXRange(0, self._length, 1)
        self.side_widget.setYRange(0, self._length, 1)



        self.top_plot.setData([0., self._width], [np.cos(self._inclination_angle*np.pi/180)*self._length, np.cos(
            self._inclination_angle*np.pi/180)*self._length])
        self.top_widget.getPlotItem().getViewBox().setLimits(
            xMin=-10, xMax=self._width + 30, yMin=-10, yMax=self._length + 30)
        self.top_widget.setXRange(0, self._width, 1)
        self.top_widget.setYRange(0, self._length, 1)
        self.top_widget.setTitle(
            'Top View -- Orientation: ' + str(self._orientation_angle) + '°')



        self.__arrow_angle = 90 + self._orientation_angle
        self.__arrow_pos = [
            self._width/2, np.cos(self._inclination_angle*np.pi/180)*self._length*0.5]
        self.arrow.setStyle(angle=self.__arrow_angle)
        self.arrow.setPos(self.__arrow_shift_to_base()[0], self.__arrow_shift_to_base()[1])
        
        self.arrow_north.setPos(self._width+15, self._length+15)

        return

    def update_inclination_angle(self, a1: int) -> None:
        self._inclination_angle = a1
        self._replot()
        return

    def update_orientation_angle(self, a2: int) -> None:
        self._orientation_angle = a2
        self._replot()
        return
    
    def update_panel_length(self,l:int) -> None:
        self._length = l
        self._replot()
        return
    
    def update_panel_width(self,w:int) -> None:
        self._width = w
        self._replot()
        return
    
    def __arrow_shift_to_base(self) -> typing.Tuple[float,float]:
        output = self.__arrow_pos.copy()
        
        #output[0] += self.arrow.opts["tailLen"]/20 * np.cos(self.__arrow_angle)
        #output[1] += self.arrow.opts["tailLen"]/20 * np.sin(self.__arrow_angle)
        return output

    # def slot_function_side(self):

    # def slot_function_sky(self):
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
