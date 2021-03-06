import typing
import pyqtgraph as pg
import csv
import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QApplication, QVBoxLayout,\
    QSizePolicy, QFileDialog, QPushButton, QGridLayout
from datetime import datetime


def loadMeteoCSV(file: str) -> typing.Tuple[typing.List[datetime], typing.List[int]]:
    dates = []  # Dates, expected to be hour-precise
    energies = []  # Energies, in Wh/m2 on one hour

    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")

        # Dump header
        reader.__next__()

        for row in reader:
            dates.append(datetime.strptime(row[0], "%d/%m/%Y %H"))
            energies.append(int(row[1]))

    return dates, energies


def aggregateByDay(dates: typing.List[datetime], energies: typing.List[int]) -> typing.Tuple[typing.List[datetime], typing.List[int]]:
    classifier: typing.Dict[datetime, int] = dict()
    assert len(dates) == len(energies)

    for i in range(len(dates)):
        dayDate = datetime(dates[i].year, dates[i].month, dates[i].day)
        if dayDate in classifier.keys():
            classifier[dayDate] += energies[i]
        else:
            classifier[dayDate] = energies[i]

    dayDate_list = list(classifier.keys())
    dayDate_list.sort()

    output_energies = []

    for d in dayDate_list:
        output_energies.append(classifier[d])

    return dayDate_list, output_energies


def aggregateByMonth(dates: typing.List[datetime], energies: typing.List[int]) -> typing.Tuple[typing.List[datetime], typing.List[int]]:
    classifier: typing.Dict[datetime, int] = dict()
    assert len(dates) == len(energies)

    for i in range(len(dates)):
        monthDate = datetime(dates[i].year, dates[i].month, 1)
        if monthDate in classifier.keys():
            classifier[monthDate] += energies[i]
        else:
            classifier[monthDate] = energies[i]

    monthDate_list = list(classifier.keys())
    monthDate_list.sort()

    output_energies = []

    for d in monthDate_list:
        output_energies.append(classifier[d])

    return monthDate_list, output_energies

#################### Widgets to display meteo data ####################
class MonthMeteoWidget(QWidget):
    def __init__(self, data_path: str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        self.data_src = data_path

        dates, energies = loadMeteoCSV(data_path)
        monthDates, monthEnergies = aggregateByMonth(dates, energies)

        layout = QGridLayout(self)

        monthWidget = pg.PlotWidget(name="monthWidget")
        monthWidget.setXRange(1, len(monthDates)+1)
        monthPlotItem: pg.PlotItem = monthWidget.getPlotItem()
        monthPlotItem.enableAutoRange()
        monthPlotItem.setLabel("left", "Energy per meter squared", "Wh/m^2")
        monthPlotItem.setLabel("bottom", "Month")
        self.barGraph = pg.BarGraphItem(
            x=range(1, len(monthDates)+1), y1=monthEnergies, width=1,
            pen=pg.mkPen(pg.mkColor((98,58,23,200)),width=2),
            brush=pg.mkBrush(pg.mkColor((239,142,56,255))))
        monthPlotItem.addItem(self.barGraph)
        monthPlotItem.getViewBox().setMouseEnabled(x=False, y=False)
        monthWidget.setFixedHeight(300)
        monthWidget.setFixedWidth(400)

        monthWidget.setSizePolicy(QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Minimum)

        layout.addWidget(monthWidget, 0, 0, 2, 2)
        
    def update(self,data_path:str):
        dates, energies = loadMeteoCSV(data_path)
        monthDates, monthEnergies = aggregateByMonth(dates, energies)
        self.barGraph.setOpts(x=range(1, len(monthDates)+1), y1=monthEnergies)
        
        
class DayMeteoWidget(QWidget):
    def __init__(self, data_path: str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        self.data_src = data_path

        dates, energies = loadMeteoCSV(data_path)
        dayDates, dayEnergies = aggregateByDay(dates, energies)

        layout = QHBoxLayout(self)

        dayWidget = pg.PlotWidget(name="dayWidget")
        dayWidget.setXRange(1, len(dayDates)+1)
        dayPlotItem: pg.PlotItem = dayWidget.getPlotItem()
        dayPlotItem.enableAutoRange()
        dayPlotItem.setLabel("left", "Energy per meter squared", "Wh/m^2")
        dayPlotItem.setLabel("bottom", "day")
        self.barGaph = pg.BarGraphItem(
            x=range(1, len(dayDates)+1), y1=dayEnergies, width=1,
            pen=pg.mkPen(pg.mkColor((62,37,14,255)),width=1/30),
            brush=pg.mkBrush(pg.mkColor((242,145,56,200))))
        dayPlotItem.addItem(self.barGaph)
        dayPlotItem.getViewBox().setMouseEnabled(x=False, y=False)
        #self.setMinimumHeight(30)
        #self.setMinimumWidth(40)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                  QSizePolicy.Policy.MinimumExpanding)

        layout.addWidget(dayWidget)
        
    def update(self,data_path:str):
        dates, energies = loadMeteoCSV(data_path)
        dayDates, dayEnergies = aggregateByDay(dates, energies)
        
        self.barGaph.setOpts(x=range(1, len(dayDates)+1), y1=dayEnergies)
        
    


def test():
    dates, energies = loadMeteoCSV("meteo.csv")
    dayDates, dayEnergies = aggregateByDay(dates, energies)
    monthDates, monthEnergies = aggregateByMonth(dates, energies)

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Meteo display test")

    mainWidget = QWidget(win)
    layout = QHBoxLayout(mainWidget)

    dayWidget = pg.PlotWidget(name="dayWidget")
    dayWidget.setXRange(1, len(dayDates)+1)
    dayPlotItem: pg.PlotItem = dayWidget.getPlotItem()
    dayPlotItem.setLabel("left", "Energy per meter squared", "Wh/m^2")
    dayPlotItem.setLabel("bottom", "Day")
    dayPlotItem.addItem(pg.BarGraphItem(
        x=range(1, len(dayDates)+1), y1=dayEnergies, width=0.1))
    dayPlotItem.getViewBox().setMouseEnabled(x=False, y=False)

    monthWidget = pg.PlotWidget(name="monthWidget")
    monthWidget.setXRange(1, len(monthDates)+1)
    monthPlotItem: pg.PlotItem = monthWidget.getPlotItem()
    monthPlotItem.setLabel("left", "Energy per meter squared", "Wh/m^2")
    monthPlotItem.setLabel("bottom", "Month")
    monthPlotItem.addItem(pg.BarGraphItem(
        x=range(1, len(monthDates)+1), y1=monthEnergies, width=1))
    monthPlotItem.getViewBox().setMouseEnabled(x=False, y=False)
    monthPlotItem.setMinimumHeight(300)
    monthPlotItem.setMinimumWidth(400)
    mainWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                             QSizePolicy.Policy.MinimumExpanding)

    layout.addWidget(dayWidget)
    layout.addWidget(monthWidget)
    mainWidget.setLayout(layout)
    win.setCentralWidget(mainWidget)

    win.show()
    sys.exit(app.exec_())


def test_monthMeteoWidget():
    
    # General PyQtGraph options
    pg.setConfigOption("background",'w')
    pg.setConfigOption("foreground",'k')
    pg.setConfigOption("antialias",True)
    
    
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("MonthMeteoWidget test window")
    win.setCentralWidget(DayMeteoWidget("meteo.csv", win))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # test()
    test_monthMeteoWidget()
