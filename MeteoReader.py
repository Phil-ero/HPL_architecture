import typing
import pyqtgraph as pg
import csv
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,QLabel,QHBoxLayout,QWidget
from datetime import datetime

def loadMeteoCSV(file:str) -> typing.Tuple[typing.List[datetime],typing.List[int]]:
    dates = [] #Dates, expected to be hour-precise
    energies = [] # Energies, in Wh/m2 on one hour
    
    with open(file,newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        # Dump header
        reader.__next__()
        
        for row in reader:
            dates.append(datetime.strptime(row[0],"%d/%m/%Y %H"))
            energies.append(int(row[1]))
            
    return dates,energies

def aggregateByDay(dates:typing.List[datetime],energies:typing.List[int]) -> typing.Tuple[typing.List[datetime],typing.List[int]]:
    classifier:typing.Dict[datetime,int] = dict()
    assert len(dates) == len(energies)
    
    for i in range(len(dates)):
        dayDate = datetime(dates[i].year,dates[i].month,dates[i].day)
        if dayDate in classifier.keys():
            classifier[dayDate] += energies[i]
        else:
            classifier[dayDate] = energies[i]
    
    dayDate_list = list(classifier.keys())
    dayDate_list.sort()
    
    output_energies = []
    
    for d in dayDate_list:
        output_energies.append(classifier[d])
        
    return dayDate_list,output_energies

def aggregateByMonth(dates:typing.List[datetime],energies:typing.List[int]) -> typing.Tuple[typing.List[datetime],typing.List[int]]:   
    classifier:typing.Dict[datetime,int] = dict()
    assert len(dates) == len(energies)
    
    for i in range(len(dates)):
        monthDate = datetime(dates[i].year,dates[i].month,1)
        if monthDate in classifier.keys():
            classifier[monthDate] += energies[i]
        else:
            classifier[monthDate] = energies[i]
    
    monthDate_list = list(classifier.keys())
    monthDate_list.sort()
    
    output_energies = []
    
    for d in monthDate_list:
        output_energies.append(classifier[d])
        
    return monthDate_list,output_energies


def test():
    dates,energies = loadMeteoCSV("meteo.csv")
    app = pg.mkQApp()
    mw = QMainWindow()
    mw.setWindowTitle('Test plot meteo')
    mw.resize(800,800)
    cw = QWidget(mw)
    mw.setCentralWidget(cw)
    l = QHBoxLayout()

    pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
    l.addWidget(pw)
    pw2 = pg.PlotWidget(name='Plot2')
    l.addWidget(pw2)
    cw.setLayout(l)
    
    pw.setLabel('left', 'Engery', units='Wh/m^2')
    pw.setLabel('bottom', 'Time', units='Day')
    pw2.setLabel('left', 'Engery', units='Wh/m^2')
    pw2.setLabel('bottom', 'Time', units='Month')

    x_f = np.array(range(1,366))
    p1 = pw.plot()
    p1.setData(y=y_f, x=x_f)
    p1.setPen((200,200,100))


    x_m_plot = range(1,14)
    pw2.plot(x_m_plot, y_m, stepMode="center", fillLevel=0, fillOutline=True, brush=(0,0,255,150))
    
    
    mw.show()
    
if __name__ == "__main__":
    test()