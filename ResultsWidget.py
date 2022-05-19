from statistics import mean
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QFormLayout, QLabel, QSizePolicy,\
    QHBoxLayout, QApplication, QMainWindow, QFrame, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QRgba64
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore
from PhysicsModel import CalcEnergy, Calc3DEnergy
import pyqtgraph as pg
import numpy as np
import typing
import sys
from MeteoReader import loadMeteoCSV, aggregateByDay
from datetime import datetime, timedelta
from water import heatedLiters, tankSatisfaction


class Color(QWidget):
    
    def __init__(self, *color) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(*color))
        self.setPalette(palette)
        self.setMinimumWidth(40)
        self.setMinimumHeight(30)

#################### Per day energy production ####################


class EnergyWidget(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, initParams: typing.List = [], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        # Model's parameters
        if initParams:
            self.panelWidth: float = initParams[0]  # cm
            self.panelHeight: float = initParams[1]  # cm
            # °, 0° is flat on the ground, 90° is standing
            self.panelInclination: float = initParams[2]
            # °, 0° is north, -90° is west, 90° is east
            self.panelOrientation: float = initParams[3]
            self.efficiency: float = initParams[4]  # [0,1]
            # °, 0 is at the equator, 90 at the North pole, -90 South pole
            self.latitude: float = initParams[5]
            self.longitude: float = initParams[6]
            # dates, with year,month,day,hour
            self.timeByHour: typing.List[datetime] = initParams[7].copy()
            # Wh/m^2
            self.receviedEnergyPerHour: typing.List[float] = initParams[8].copy()
        else:
            self.panelWidth: float = 100  # cm
            self.panelHeight: float = 100  # cm
            self.panelInclination: float = 0  # °, 0° is flat on the ground, 90° is standing
            self.panelOrientation: float = 180  # °, 0° is north, -90° is west, 90° is east
            self.efficiency: float = 0.3  # [0,1]
            # °, 0 is at the equator, 90 at the North pole, -90 South pole
            self.latitude: float = 46.204
            self.longitude: float = 6.142
            self.timeByHour: typing.List[datetime] = [datetime(
                2002, 1, 1, 0) + timedelta(hours=i) for i in range(365*24)]  # dates, with year,month,day,hour
            self.receviedEnergyPerHour: typing.List[float] = [
                0]*365*24  # Wh/m^2

        self.energyPerDay: typing.List[float] = [0]*365  # Wh

        # Graph
        layout = QGridLayout(self)
        self.energyPlotWidget = pg.PlotWidget(name="energyWidget")
        self.energyPlotWidget.setXRange(1, len(self.energyPerDay)+1)
        self.energyPlotWidget.setYRange(0, 1000000)
        self.energyPlotItem: pg.PlotItem = self.energyPlotWidget.getPlotItem()
        self.energyPlotItem.setLabel("left", "Energy", "Wh")
        self.energyPlotItem.setLabel("bottom", "Day")
        self.energyBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.energyPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((50, 84, 244, int(0.8*255))), width=2),
            brush=pg.mkBrush(pg.mkColor((50, 218, 244, int(0.8*255)))))
        self.energyPlotItem.addItem(self.energyBarGraph)
        self.energyPlotItem.getViewBox().setMouseEnabled(x=False, y=False)
        # self.energyPlotWidget.setMininmumHeight(150)
        # self.energyPlotWidget.setMininmumWidth(200)
        self.energyPlotWidget.setTitle("Energy produced each day")

        self.energyPlotWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                            QSizePolicy.Policy.MinimumExpanding)

        layout.addWidget(self.energyPlotWidget, 0, 0, 2, 2)

        self._replot()

    def _replot(self) -> None:

        # Do conversions for units when calling model function
        """
        energyPerHour = CalcEnergy(self.panelHeight/100, self.panelWidth/100,
                                   self.panelInclination,
                                   self.panelOrientation,
                                   self.efficiency,
                                   self.latitude,
                                   self.receviedEnergyPerHour)
        """
        energyPerHour = Calc3DEnergy(self.panelHeight/100,self.panelWidth/100,
                                     self.panelInclination,self.panelOrientation,
                                     self.efficiency,self.latitude,self.longitude,
                                     self.timeByHour,self.receviedEnergyPerHour)

        _, self.energyPerDay = aggregateByDay(self.timeByHour, energyPerHour)

        if max(self.energyPerDay) > 1000000:
            self.energyPlotWidget.setYRange(0, max(self.energyPerDay)*1.05)
        else:
            self.energyPlotWidget.setYRange(0, 1000000)

        self.energyBarGraph.setOpts(y1=self.energyPerDay)
        self.valueChanged.emit()

    def update_panel_width(self, w: float) -> None:
        self.panelWidth = w
        self._replot()

    def update_panel_height(self, h: float) -> None:
        self.panelHeight = h
        self._replot()

    def update_panel_inclination(self, i: float) -> None:
        self.panelInclination = i
        self._replot()

    def update_panel_orientation(self, o: float) -> None:
        self.panelOrientation = o
        self._replot()

    def update_efficiency(self, e: float) -> None:
        self.efficiency = e
        self._replot()

    def update_latitude(self, l: float) -> None:
        self.latitude = l
        self._replot()
        
    def update_longitude(self, l:float) -> None:
        self.longitude = l
        self._replot()
        
    def update_time_by_hour(self,l:typing.List[datetime]) -> None:
        self.timeByHour = l.copy()
        self._replot()

    def update_received_energy(self, l: typing.List[float]) -> None:
        self.receviedEnergyPerHour = l.copy()
        self._replot()


#################### Per day needs satisfaction ####################

class SatisfactionWidget(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        # Model's parameters
        self.volumeWanted: int = 100  # L
        self.entryTemperature: int = 10  # °C
        self.exitTemperature: int = 35  # °C

        self.waterTankEnabled: bool = False
        self.waterTankCapacity: float = 0  # L

        self.energyPerDay: typing.List[float] = [0]*365  # Wh

        self.panelPerDay: typing.List[float] = [0]*365 # L
        self.tankVolumePerDay: typing.List[float] = [0]*365  # L
        self.wastedPerDay: typing.List[float] = [0]*365 # Percentage
        self.tankFillPerDay: typing.List[float] = [0]*365 # Percentage
        self.tankEmptyPerDay: typing.List[float] = [0]*365 # Percentage
        self.panelSatisfactionPerDay: typing.List[float] = [0]*365 # Percentage
        
        # Graph display
        
        self.wastedColor = pg.mkColor((232, 26, 26, int(0.9*255)))
        self.wastedBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.wastedPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0, 0, 0, int(0.05*255))), width=2),
            brush=pg.mkBrush(self.wastedColor))

        self.tankFillColor = pg.mkColor((39, 110, 245, int(0.9*255)))
        self.tankFillBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.tankFillPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0, 0, 0, int(0.05*255))), width=2),
            brush=pg.mkBrush(self.tankFillColor))

        self.tankEmptyColor = pg.mkColor((244, 234, 50, int(0.9*255)))
        self.tankEmptyBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.tankEmptyPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0, 0, 0, int(0.05*255))), width=2),
            brush=pg.mkBrush(self.tankEmptyColor))

        self.panelColor = pg.mkColor((26, 232, 54, int(0.9*255)))
        self.panelBarGraph: pg.BarGraphItem = pg.BarGraphItem(
            x=range(1, len(self.energyPerDay)+1), y1=self.panelSatisfactionPerDay, width=1,
            pen=pg.mkPen(pg.mkColor((0, 0, 0, int(0.05*255))), width=2),
            brush=pg.mkBrush(self.panelColor))

        # Putting graphs together in a plot
        
        layout = QGridLayout(self)

        self.plotWidget = pg.PlotWidget(name='satisfaction')
        self.plotWidget.getPlotItem().getViewBox().setLimits(
            xMin=0, xMax=366, yMin=0, yMax=2)
        self.plotWidget.setXRange(0, 365, 1)
        self.plotWidget.setMouseEnabled(x=False, y=False)
        self.satisfactionLine: pg.PlotDataItem = self.plotWidget.plot(
            [0, 366],
            [1, 1],
            pen=pg.mkPen(color='k', width=0.8))

        self.plotWidget.addItem(self.wastedBarGraph)
        self.plotWidget.addItem(self.tankFillBarGraph)
        self.plotWidget.addItem(self.tankEmptyBarGraph)
        self.plotWidget.addItem(self.panelBarGraph)

        self.plotWidget.showGrid(x=False, y=True)
        self.plotWidget.setTitle("Hot water supply's breakdown")
        self.plotWidget.setLabel('bottom', "Day")
        self.plotWidget.setLabel('left', "Proportion of water provided")
        self.plotWidget.setMinimumWidth(200)
        self.plotWidget.setMinimumHeight(200)

        self.plotWidget.setSizePolicy(QSizePolicy.Policy.Minimum,
                                      QSizePolicy.Policy.Minimum)

        layout.addWidget(self.plotWidget,0,0,2,2)
        
        # Add legend
        
        legendWidget = QWidget(self)
        legendLayout = QFormLayout(legendWidget)
        
        self.panelFrame = Color(self.panelColor)
        legendLayout.addRow(self.panelFrame,QLabel("Solar panel direct use"))
        
        self.tankEmptyFrame = Color(self.tankEmptyColor)
        legendLayout.addRow(self.tankEmptyFrame,QLabel("Tank water used"))
        
        self.tankFillFrame = Color(self.tankFillColor)
        legendLayout.addRow(self.tankFillFrame,QLabel("Filling tank"))
        
        self.wastedFrame = Color(self.wastedColor)
        legendLayout.addRow(self.wastedFrame,QLabel("Wasted output"))
        
        layout.addWidget(legendWidget,0,2,2,1)
        
        self._replot()

    def _replot(self) -> None:

        # Reset all graphs
        self.panelPerDay.clear()
        self.tankVolumePerDay.clear()
        self.wastedPerDay.clear()
        self.tankFillPerDay.clear()
        self.tankEmptyPerDay.clear()
        self.panelSatisfactionPerDay.clear()
        
        self.wastedBarGraph.setOpts(y1=[0]*365)
        self.tankFillBarGraph.setOpts(y1=[0]*365)
        self.tankEmptyBarGraph.setOpts(y1=[0]*365)
        self.panelBarGraph.setOpts(y1=[0]*365)

        if self.waterTankEnabled:
            self.tankVolumePerDay, self.panelPerDay = tankSatisfaction(
                self.entryTemperature, self.exitTemperature, self.volumeWanted, self.waterTankCapacity, self.energyPerDay)
            
            producedPerDay = [p/self.volumeWanted for p in self.panelPerDay]
            tankValues = [t/self.volumeWanted for t in self.tankVolumePerDay]
            deltaTanks = [tankValues[i+1] - tankValues[i] for i in range(len(self.tankVolumePerDay)-1)]
            self.panelSatisfactionPerDay = [p/self.volumeWanted for p in self.panelPerDay]
            
            overflowBarVals = []
            tankFillBarVals = []
            tankEmptyBarVals = []
            panelBarVals = [p if p < 1 else 1 for p in producedPerDay]
            
            for i in range(len(producedPerDay)):
                if 1+deltaTanks[i] < producedPerDay[i]:
                    overflowBarVals.append(producedPerDay[i])
                    self.wastedPerDay.append(producedPerDay[i] - 1 - deltaTanks[i])
                else:
                    overflowBarVals.append(0)
                    self.wastedPerDay.append(0)
                    
                if deltaTanks[i] > 0:
                    self.tankFillPerDay.append(deltaTanks[i])
                    tankFillBarVals.append(1 + deltaTanks[i])
                    self.tankEmptyPerDay.append(0)
                    tankEmptyBarVals.append(0)
                elif deltaTanks[i] < 0:
                    self.tankFillPerDay.append(0)
                    tankFillBarVals.append(0)
                    self.tankEmptyPerDay.append(-deltaTanks[i])
                    tankEmptyBarVals.append(producedPerDay[i]-deltaTanks[i])
                else:
                    self.tankFillPerDay.append(0)
                    self.tankEmptyPerDay.append(0)
                    tankFillBarVals.append(0)
                    tankEmptyBarVals.append(0)
                    
                
            self.wastedBarGraph.setOpts(y1=overflowBarVals)
            self.tankFillBarGraph.setOpts(y1=tankFillBarVals)
            self.tankEmptyBarGraph.setOpts(y1=tankEmptyBarVals)
            self.panelBarGraph.setOpts(y1=panelBarVals)

        else:
            self.panelPerDay = [heatedLiters(
                self.entryTemperature, self.exitTemperature, e) for e in self.energyPerDay]

            wasterBarVals = [p/self.volumeWanted if p > self.volumeWanted else 0 for p in self.panelPerDay]
            self.panelSatisfactionPerDay = [
                1 if p > self.volumeWanted else p/self.volumeWanted for p in self.panelPerDay]

            self.wastedPerDay = [p/self.volumeWanted - 1 if p > self.volumeWanted else 0 for p in self.panelPerDay]

            self.wastedBarGraph.setOpts(y1=wasterBarVals)
            self.panelBarGraph.setOpts(y1=self.panelSatisfactionPerDay)

        self.valueChanged.emit()

    def update_volume_wanted(self, v: float) -> None:
        self.volumeWanted = v
        self._replot()

    def update_temperatures(self, temps: typing.Tuple[float, float]) -> None:
        self.entryTemperature = temps[0]
        self.exitTemperature = temps[1]
        self._replot()

    def update_water_tank(self, enable: bool, c: float) -> None:
        self.waterTankEnabled = enable
        self.waterTankCapacity = c
        self._replot()

    def update_energyPerDay(self, energies: typing.List[float]) -> None:
        self.energyPerDay = energies.copy()
        self._replot()


#################### Additional feedback ####################
class SerieBreakdown(QFrame):
    def __init__(self, serie:typing.List[float], name:str, unit:str=None, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        
        # Declare attributes
        self.serie:typing.List[float] = serie
        self.unit = unit
        
        self.minVal:float 
        self.maxVal:float 
        self.avgVal:float 
        self.stdVal:float 
        
        # Declare widgets
        
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(name,self))
        subwidget = QWidget(self)
        
        sublayout = QFormLayout(subwidget)
        
        self.rangeLabel = QLabel(subwidget)
        self.avgLabel = QLabel(subwidget)
        
        sublayout.addRow("- [Min,Max]:",self.rangeLabel)
        sublayout.addRow("- Average ± σ:",self.avgLabel)
        
        subwidget.setLayout(sublayout)
        
        layout.addWidget(subwidget)
        self.setLayout(layout)
        
        # Update values
        self.update(serie)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Minimum)
        
    def update(self,s:typing.List[float]):
        self.serie = s
        self.minVal = float(min(self.serie))
        self.maxVal = float(max(self.serie))
        self.avgVal = float(mean(self.serie))
        self.stdVal = float(np.std(self.serie))
        
        if self.unit:
            if self.minVal > 10**9:
                self.rangeLabel.setText(f"[ {self.minVal/10**9:.2f} , {self.maxVal/10**9:.2f} ] G{self.unit}")
                self.avgLabel.setText(f"{self.avgVal/10**9:.2f} ± {self.stdVal/10**9:.2f} G{self.unit}")
            elif self.minVal > 10**6:
                self.rangeLabel.setText(f"[ {self.minVal/10**6:.2f} , {self.maxVal/10**6:.2f} ] M{self.unit}")
                self.avgLabel.setText(f"{self.avgVal/10**6:.2f} ± {self.stdVal/10**6:.2f} M{self.unit}")
            elif self.minVal > 10**3:
                self.rangeLabel.setText(f"[ {self.minVal/10**3:.2f} , {self.maxVal/10**3:.2f} ] k{self.unit}")
                self.avgLabel.setText(f"{self.avgVal/10**3:.2f} ± {self.stdVal/10**3:.2f} k{self.unit}")
            else:
                self.rangeLabel.setText(f"[ {self.minVal:.2f} , {self.maxVal:.2f} ] {self.unit}")
                self.avgLabel.setText(f"{self.avgVal:.2f} ± {self.stdVal:.2f} {self.unit}")
        else:
            self.rangeLabel.setText(f"[ {self.minVal*100:.2f} , {self.maxVal*100:.2f} %]")
            self.avgLabel.setText(f"{self.avgVal*100:.2f} ± {self.stdVal*100:.2f} %")
        

class AdditionalFeedback(QScrollArea):
    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        self.setFrameStyle(1) # Box style
        
        # Get parameters
        
        self.energyPerDay: typing.List[float] = [0]*365  # Wh

        self.panelPerDay: typing.List[float] = [0]*365 # L
        self.tankVolumePerDay: typing.List[float] = [0]*365  # L
        self.wastedPerDay: typing.List[float] = [0]*365 # Percentage
        self.tankFillPerDay: typing.List[float] = [0]*365 # Percentage
        self.tankEmptyPerDay: typing.List[float] = [0]*365 # Percentage
        self.panelSatisfactionPerDay: typing.List[float] = [0]*365 # Percentage
        
        self.totalSatisfactionPerDay: typing.List[float] = np.array(self.panelSatisfactionPerDay) + np.array(self.tankEmptyPerDay)

        # Declare wwidgets
        layout = QVBoxLayout(self)
        
        titleWidget = QFrame(self)
        titleLayout = QGridLayout(titleWidget)
        titleText = QLabel("Breakdown of several daily quantities",titleWidget)
        titleText.setStyleSheet("font-weight: bold")
        titleLayout.addWidget(titleText)
        titleWidget.setFrameShape(0x6)
    
        self.energyWidget = SerieBreakdown(self.energyPerDay,"Energy produced", "Wh",self)
        self.energyWidget.setFrameShape(0x6) 
        self.volumeProducedWidget = SerieBreakdown(self.panelPerDay,"Volume of hot water produced", "L",self)
        self.volumeProducedWidget.setFrameShape(0x6)
        self.tankVolumeWidget = SerieBreakdown(self.tankVolumePerDay,"Volume of hot water in the tank", "L",self)
        self.tankVolumeWidget.setFrameShape(0x6)
        self.satisfactionWidget = SerieBreakdown(self.totalSatisfactionPerDay, "Satisfaction",parent=self)
        self.satisfactionWidget.setFrameShape(0x6)
        self.wastedWidget = SerieBreakdown(self.wastedPerDay, "Proportion of produced water wasted ",parent=self)
        self.wastedWidget.setFrameShape(0x6)
        
        # Add them to layout
        layout.addWidget(titleWidget)
        layout.addWidget(self.energyWidget)
        layout.addWidget(self.volumeProducedWidget)
        layout.addWidget(self.tankVolumeWidget)
        layout.addWidget(self.satisfactionWidget)
        layout.addWidget(self.wastedWidget)
        
        container = QWidget()
        container.setLayout(layout)
        self.setWidget(container)
        
        #self.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.MinimumExpanding) 
    
    
    def update_energyPerDay(self,l:typing.List[float]):
        self.energyPerDay = l
        self.energyWidget.update(l)
        
    def update_panelPerDay(self,l:typing.List[float]):
        self.panelPerDay = l
        self.volumeProducedWidget.update(l)
        
    def update_tankVolumePerDay(self,l:typing.List[float]):
        self.tankVolumePerDay = l
        self.tankVolumeWidget.update(l)
        
    def update_panelSatisfaction(self,l:typing.List[float]):
        self.panelSatisfactionPerDay = l
        self.totalSatisfactionPerDay: typing.List[float] = np.array(self.panelSatisfactionPerDay) + np.array(self.tankEmptyPerDay)
        self.satisfactionWidget.update(self.totalSatisfactionPerDay)
        
    def update_tankEmpty(self,l:typing.List[float]):
        self.tankEmptyPerDay = l
        self.totalSatisfactionPerDay: typing.List[float] = np.array(self.panelSatisfactionPerDay) + np.array(self.tankEmptyPerDay)
        self.satisfactionWidget.update(self.totalSatisfactionPerDay)
        
    def update_wasted(self,l:typing.List[float]):
        self.wastedPerDay = l
        self.wastedWidget.update(l)
        


#################### Main results widget ####################
class ResultsWidget(QWidget):
    def __init__(self, energyInit: typing.List = [], satisfactionInit: typing.List = [], additionalInit: typing.List = [], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout()

        if energyInit:
            self.energyWidget = EnergyWidget(energyInit, self)
        else:
            self.energyWidget = EnergyWidget(parent=self)
        self.satisfactionWidget = SatisfactionWidget()
        self.additionalFeedbackWidget = AdditionalFeedback()

        self.energyWidget.valueChanged.connect(self._energies_handler)
        self.satisfactionWidget.valueChanged.connect(self._satisfactionWidget_handler)

        layout.addWidget(self.energyWidget)
        layout.addWidget(self.satisfactionWidget)
        layout.addWidget(self.additionalFeedbackWidget)

        self.setLayout(layout)

    def _energies_handler(self) -> None:
        self.satisfactionWidget.update_energyPerDay(
            self.energyWidget.energyPerDay)
        self.additionalFeedbackWidget.update_energyPerDay(self.energyWidget.energyPerDay)
        
    def _panelPerDay_handler(self) -> None:
        self.additionalFeedbackWidget.update_panelPerDay(self.satisfactionWidget.panelPerDay)
        
    def _tankVolumePerday_handler(self) -> None:
        self.additionalFeedbackWidget.update_tankVolumePerDay(self.satisfactionWidget.tankVolumePerDay)
        
    def _panelSatisfaction_handler(self) -> None:
        self.additionalFeedbackWidget.update_panelSatisfaction(self.satisfactionWidget.panelSatisfactionPerDay)
        
    def _tankEmpty_handler(self) -> None:
        self.additionalFeedbackWidget.update_tankEmpty(self.satisfactionWidget.tankEmptyPerDay)
        
    def _tankFill_handler(self) -> None:
        #self.satisfactionWidget.tankFillPerDay
        return
    
    def _wasted_handler(self) -> None:
        self.additionalFeedbackWidget.update_wasted(self.satisfactionWidget.wastedPerDay)
    
    def _satisfactionWidget_handler(self) -> None:
        self._panelPerDay_handler()
        self._tankVolumePerday_handler()
        self._panelSatisfaction_handler()
        self._tankEmpty_handler()
        self._tankFill_handler()
        self._wasted_handler()


def test():
    dates, energies = loadMeteoCSV("meteo.csv")

    # General PyQtGraph options
    pg.setConfigOption("background", 'w')
    pg.setConfigOption("foreground", 'k')
    pg.setConfigOption("antialias", True)

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Results window test")
    win.setCentralWidget(ResultsWidget(
        [300, 300, 90, 180, 0.6, 0.1,0.1, dates, energies], [], [], win))
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
