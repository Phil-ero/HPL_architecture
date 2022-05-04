"""
Demonstrates use of PlotWidget class. This is little more than a 
GraphicsView with a PlotItem placed in its center.
"""

import numpy as np
from datetime import datetime
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

def calc_solar():
    # get data from .csv
    data= pd.read_csv("meteo.csv",delimiter=";")
    col =data.columns
    time =data.Time 
    Energy = data.Igl_h
    # data in day format
    y = np.array(Energy)
    y_f = []
    for i  in range(0,len(y),24):
        sum_i = sum(y[i:i+24])
        y_f.append(sum_i) 
    y_f = np.array(y_f)
    x = [datetime.strptime(a,'%d/%m/%Y %H') for a in time]
    x_f = x[0:len(x):24]
    # data in month format
    idx_m = [x_f[i].month for i in range(0,len(x_f))]
    y_m = np.zeros(12)
    for i in range(len(y_f)):
        y_m[idx_m[i]-1] += y_f[i]
    x_m = np.array(range(1,13))
    return x_f,y_f,x_m,y_m



app = pg.mkQApp()
mw = QtWidgets.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800,800)
cw = QtWidgets.QWidget()
mw.setCentralWidget(cw)
l = QtWidgets.QHBoxLayout()
cw.setLayout(l)

pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
l.addWidget(pw)
pw2 = pg.PlotWidget(name='Plot2')
l.addWidget(pw2)

mw.show()

x_f,y_f,x_m,y_m = calc_solar()
x_f = np.array(range(1,366))
p1 = pw.plot()
p1.setData(y=y_f, x=x_f)
p1.setPen((200,200,100))


x_m_plot = range(1,14)
pw2.plot(x_m_plot, y_m, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))


pw.setLabel('left', 'Engery', units='Wh/m^2')
pw.setLabel('bottom', 'Time', units='Day')
pw2.setLabel('left', 'Engery', units='Wh/m^2')
pw2.setLabel('bottom', 'Time', units='Month')
 
if __name__ == '__main__':
    pg.exec()


# see examples
# import pyqtgraph.examples
# pyqtgraph.examples.run()