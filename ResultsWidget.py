from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QFormLayout, QLabel, QSizePolicy,\
    QHBoxLayout, QApplication, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore
from PhysicsModel import CalcEnergy
import pyqtgraph as pg
import numpy as np
import typing
import sys
from MeteoReader import loadMeteoCSV, aggregateByDay
from datetime import datetime, timedelta

#################### Per day energy production ####################

class EnergyWidget(QWidget):
    valueChanged = pyqtSignal()
    
    def __init__(self,initParams:typing.List = [], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        
        # Model's parameters
        if initParams:
            self.panelWidth:float = initParams[0] #cm
            self.panelHeight:float = initParams[1] #cm
            self.panelInclination:float = initParams[2] #°, 0° is flat on the ground, 90° is standing
            self.panelOrientation:float = initParams[3] #°, 0° is north, -90° is west, 90° is east
            self.efficiency:float = initParams[4] # [0,1]
            self.latitude:float = initParams[5] #°, 0 is at the equator, 90 at the North pole, -90 South pole
            self.timeByHour:typing.List[datetime] = initParams[6].copy() # dates, with year,month,day,hour
            self.receviedEnergyPerHour:typing.List[float] = initParams[7].copy() #Wh/m^2
        else:
            self.panelWidth:float = 100 #cm
            self.panelHeight:float = 100 #cm
            self.panelInclination:float = 0 #°, 0° is flat on the ground, 90° is standing
            self.panelOrientation:float = 180 #°, 0° is north, -90° is west, 90° is east
            self.efficiency:float = 0.3 # [0,1]
            self.latitude:float = 40.6 #°, 0 is at the equator, 90 at the North pole, -90 South pole
            self.timeByHour:typing.List[datetime] = [datetime(2002,1,1,0) + timedelta(hours=i) for i in range(365*24)] # dates, with year,month,day,hour
            self.receviedEnergyPerHour:typing.List[float] = [0]*365*24 #Wh/m^2
        
        self.energyPerDay:typing.List[float] = [15]*365 #Wh
        

        # Graph        
        layout = QGridLayout(self)
        self.energyPlotWidget = pg.PlotWidget(name="energyWidget")
        self.energyPlotWidget.setXRange(1,len(self.energyPerDay)+1)
        self.energyPlotItem: pg.PlotItem = self.energyPlotWidget.getPlotItem()
        self.energyPlotItem.enableAutoRange()
        self.energyPlotItem.setLabel("left", "Energy", "Wh")
        self.energyPlotItem.setLabel("bottom", "Day")
        self.energyBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.energyPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((50,84,244,0.8*255)),width=2),
            brush=pg.mkBrush(pg.mkColor((50,218,244,0.8*255))))
        self.energyPlotItem.addItem(self.energyBarGraph)
        self.energyPlotItem.getViewBox().setMouseEnabled(x=False, y=False)
        #self.energyPlotWidget.setMininmumHeight(150)
        #self.energyPlotWidget.setMininmumWidth(200)

        self.energyPlotWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                  QSizePolicy.Policy.MinimumExpanding)

        layout.addWidget(self.energyPlotWidget, 0, 0, 2, 2)
        
        self._replot()
        
    def _replot(self) -> None:
        # Do conversions for units when calling model function
        energyPerHour = CalcEnergy(self.panelHeight/100,self.panelWidth/100,
                                       self.panelInclination,
                                       180 - self.panelOrientation,
                                       self.efficiency,
                                       self.latitude,
                                       self.receviedEnergyPerHour)
        
        _,self.energyPerDay = aggregateByDay(self.timeByHour,energyPerHour)
        
        self.energyBarGraph.setOpts(y1=self.energyPerDay)
        self.valueChanged.emit()
        
    def update_panel_width(self,w:float) -> None:
        self.panelWidth = w
        self._replot()
        
    def update_panel_height(self,h:float) -> None:
        self.panelHeight = h
        self._replot()
        
    def update_panel_inclination(self,i:float) -> None:
        self.panelInclination = i
        self._replot()
        
    def update_panel_orientation(self,o:float) -> None:
        self.panelOrientation = o
        self._replot()
        
    def update_efficiency(self,e:float) -> None:
        self.efficiency = e
        self._replot()
        
    def update_latitude(self,l:float) -> None:
        self.latitude = l
        self._replot()
        
    def update_received_energy(self,l:typing.List[float]) -> None:
        self.receviedEnergyPerDay = l.copy()
        self._replot()
        

#################### Per day needs satisfaction ####################

class SatisfactionWidget(QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        
        # Model's parameters
        self.volumeWanted:int = 100 #L
        self.entryTemperature:int = 10 #°C
        self.exitTemperature:int = 35 #°C
        
        self.waterTankEnabled:bool = False
        self.waterTankCapacity:float = 0 #L 
        
        self.energyPerDay:typing.List[float] = [0]*365 #Wh
        
        self.waterTankVolumePerDay:typing.List[float] = [0]*365 #L
        self.satisfactionPerDay:typing.List[float] = [0]*365 # Percentage
        
        self.wastedPerDay:typing.List[float] = [0]*365
        self.oversatisfiedPerDay:typing.List[float] = [0]*365
        self.missingSatisfactionPerDay:typing.List[float] = [1.0]*365
        self.tankSatisfactionPerDay:typing.List[float] = [0]*365
        self.panelSatisfactionPerDay:typing.List[float] = [0]*365
        
        self.wastedBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.wastedPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0,0,0,int(0.65*255))),width=2),
            brush=pg.mkBrush(pg.mkColor((232,26,26,int(0.8*255)))))
        
        self.oversatisfiedBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.oversatisfiedPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0,0,0,int(0.65*255))),width=2),
            brush=pg.mkBrush(pg.mkColor((39,110,245,int(0.8*255)))))
        
        self.missingBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.missingSatisfactionPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0,0,0,int(0.65*255))),width=2),
            brush=pg.mkBrush(pg.mkColor((232,26,26,int(0.8*255)))))
        
        self.tankBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.tankSatisfactionPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0,0,0,int(0.65*255))),width=2),
            brush=pg.mkBrush(pg.mkColor((244,234,50,int(0.8*255)))))
        
        self.panelBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.panelSatisfactionPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0,0,0,int(0.65*255))),width=2),
            brush=pg.mkBrush(pg.mkColor((26,232,54,int(0.8*255)))))
        
        
        
        layout = QGridLayout(self)
        """
        self.monthWidget = pg.PlotWidget(name="satisfactionWidget")
        self.monthWidget.setXRange(1, len(self.energyPerDay)+1)
        self.monthPlotItem: pg.PlotItem = self.monthWidget.getPlotItem()
        self.monthPlotItem.enableAutoRange()
        self.monthPlotItem.setLabel("left", "Energy per meter squared", "Wh/m^2")
        self.monthPlotItem.setLabel("bottom", "Month")
        self.monthPlotItem.addItem(pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=monthEnergies, width=1,
            pen=pg.mkPen(pg.mkColor((98,58,23,200)),width=2),
            brush=pg.mkBrush(pg.mkColor((239,142,56,255)))))
        monthPlotItem.getViewBox().setMouseEnabled(x=False, y=False)
        monthWidget.setFixedHeight(300)
        monthWidget.setFixedWidth(400)

        monthWidget.setSizePolicy(QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Minimum)

        layout.addWidget(monthWidget, 0, 0, 2, 2)
        """

#################### Additional feedback ####################

class AdditionalFeedback(QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        
        layout = QFormLayout(self)
        
        
        # Declare different values
        self.totalEnergy:float = 0.0
        
        self.avgEnergy:float = 0.0
        self.avgEnergyLabel = QLabel(f"{self.avgEnergy:.2} Wh/day",self)
        
        self.missingEnergy:float = 0.0
        self.missingEnergyLabel = QLabel(f"{self.missingEnergy:.2} Wh",self)
        
        self.missingWater:float = 0.0
        self.missingWaterLabel = QLabel(f"{self.missingWater:.2} L",self)
        
        self.overflowedEnergy:float = 0.0
        self.overflowedEnergyLabel = QLabel(f"{self.overflowedEnergy:.2} Wh",self)
        
        self.overflowedProportion:float = 0.0
        self.overflowedProportionLabel = QLabel(f"{self.overflowedProportion:2.2%}",self)
        
        
        # Add them to layout
        layout.addRow("Average energy produced per day",self.avgEnergyLabel)
        layout.addRow("Quantity of energy missing",self.missingEnergyLabel)
        layout.addRow("Liters of hot water missing",self.missingWaterLabel)
        layout.addRow("Wasted energy",self.overflowedEnergyLabel)
        layout.addRow("Wasted energy (proportion)",self.overflowedProportionLabel)


#################### Main results widget ####################
class ResultsWidget(QWidget):
    def __init__(self, energyInit:typing.List = [], satisfactionInit:typing.List = [], additionalInit:typing.List = [], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        
        layout = QHBoxLayout()
        
        if energyInit:
            self.energyWidget = EnergyWidget(energyInit,self)
        else:
            self.energyWidget = EnergyWidget(parent=self)
        self.satisfactionWidget = SatisfactionWidget()
        self.additionalFeedbackWidget = AdditionalFeedback()
        
        layout.addWidget(self.energyWidget)
        layout.addWidget(self.satisfactionWidget)
        layout.addWidget(self.additionalFeedbackWidget)
        
        self.setLayout(layout)
        
        
def test():
    dates,energies = loadMeteoCSV("meteo.csv")
    
    # General PyQtGraph options
    pg.setConfigOption("background",'w')
    pg.setConfigOption("foreground",'k')
    pg.setConfigOption("antialias",True)
    
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Results window test")
    win.setCentralWidget(ResultsWidget([300,300,90,180,0.6,0.1,dates,energies],[],[],win))
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()