import sys
import typing
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QMainWindow, QPushButton, QLabel,\
    QTabWidget, QVBoxLayout, QSizePolicy, QCheckBox
from PyQt5.QtGui import QPalette, QColor, QRgba64
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import pyqtgraph as pg

from ParametersWidget import ParametersWidget, HBoxSlider, VBoxSlider, VRangeSlider, HFloatSlider, VFloatSlider
from Section import Section
from MeteoReader import DayMeteoWidget,MonthMeteoWidget, loadMeteoCSV
from ParametersWidget import OrientationWidget,HBoxSlider
from Solarvizu import Solar_Panel
from ResultsWidget import ResultsWidget

class Color(QWidget):
    
    def __init__(self, *color) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(*color))
        self.setPalette(palette)
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

class TabContent(QWidget):

    ##### Build the widget #####
    
    def _MakeParameterWidgets(self,introText:str) -> None:
        parameterWidgetsList:typing.List[QWidget] = []
        """
        ## Introductory text
        introTextSection = Section(title="Presentation",parent=self)
        introTextSectionLayout = QGridLayout(introTextSection.contentArea)
        introTextSectionLayout.addWidget(QLabel(introText,introTextSection.contentArea))
        introTextSection.setContentLayout(introTextSectionLayout)
        
        introTextSection.setMinimumWidth(introTextSectionLayout.itemAt(0).widget().sizeHint().width())
        parameterWidgetsList.append(introTextSection)
        """
        
        ## Localisation
        
        localisationSection = Section(title="Localisation", parent=self)
        localisationLayout = QGridLayout(localisationSection.contentArea)
        
        # Widgets
        self.latitudeWidget = VFloatSlider(-90000,90000,3,"Latitude","°")
        self.latitudeWidget.valueChanged.connect(self._latitude_handler)
        self.longitudeWidget = HFloatSlider(-180000,180000,3,"Longitude","°")
        self.longitudeWidget.valueChanged.connect(self._longitude_handler)
        
        # Layout
        
        localisationLayout.addWidget(self.latitudeWidget,1,0,2,1)
        localisationLayout.addWidget(self.longitudeWidget,0,0,1,2)
        localisationSection.setContentLayout(localisationLayout)
        localisationSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        parameterWidgetsList.append(localisationSection)
        
        
        ## Meteo
        meteoSection = Section(title="Meteo",parent=self)
        meteoSectionLayout = QGridLayout(meteoSection.contentArea)
        meteoSectionLayout.addWidget(MonthMeteoWidget(self.meteo_file))
        meteoSection.setContentLayout(meteoSectionLayout)
        
        meteoSection.setMinimumWidth(meteoSectionLayout.itemAt(0).widget().sizeHint().width())
        parameterWidgetsList.append(meteoSection)
        
        ## Solar panel
        # Declare section and layout
        solarPanelSection = Section("Solar panel")
        solarPanelLayout = QVBoxLayout(solarPanelSection.contentArea)
        
        # Declare widgets and connect them to signal handlers
        self.inclinationAngleWidget = HBoxSlider(0,90,1,"Inclination angle:","°")
        self.inclinationAngleWidget.valueChanged.connect(self._inclination_angle_handler)
        
        self.orientationAngleWidget = OrientationWidget(solarPanelSection)
        self.orientationAngleWidget.valueChanged.connect(self._orientation_angle_handler)
        
        self.solarPanelWidthWidget = HBoxSlider(1,500,1,"Width:","cm")
        self.solarPanelWidthWidget.valueChanged.connect(self._width_handler)
        
        self.solarPanelHeightWidget = HBoxSlider(1,500,1,"Height:","cm")
        self.solarPanelHeightWidget.valueChanged.connect(self._height_handler)
        
        self.solarPanelEfficiencyWidget = HBoxSlider(1,100,1,"Efficiency",'%')
        self.solarPanelEfficiencyWidget.valueChanged.connect(self._efficiency_handler)
        
        # Add widgets to layout
        solarPanelLayout.addWidget(self.inclinationAngleWidget)
        solarPanelLayout.addWidget(self.orientationAngleWidget)
        solarPanelLayout.addWidget(self.solarPanelWidthWidget)
        solarPanelLayout.addWidget(self.solarPanelHeightWidget)
        solarPanelLayout.addWidget(self.solarPanelEfficiencyWidget)
        solarPanelSection.setContentLayout(solarPanelLayout)
        solarPanelSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        # Add Section to list
        parameterWidgetsList.append(solarPanelSection)
        
        ## Boiler
        # Declare section and layout
        
        boilerSection = Section("Boiler")
        boilerLayout = QVBoxLayout(boilerSection.contentArea)
        
        # Declare widgets and connect them
        self.boilerConsumptionWidget = VBoxSlider(0,500,1,"Hot water consumption", "L/day")
        self.boilerConsumptionWidget.valueChanged.connect(self._water_consumption_handler)
        
        self.boilerTemperaturesWidget = VRangeSlider(0,100,1,"Water output temperature", "Water input temperature","°C")
        self.boilerTemperaturesWidget.valueChanged.connect(self._water_temperature_handler)
        
        self.boilerCapEnableWidget = QCheckBox("Hot water storage tank")
        self.boilerCapEnableWidget.setChecked(False)
        self.boilerCapEnableWidget.toggled.connect(self._boiler_capacity_enable_handler)
        
        self.boilerCapacityWidget = HBoxSlider(0,500,1,"Tank's capacity", "L")
        self.boilerCapacityWidget.setDisabled(True)
        self.boilerCapacityWidget.valueChanged.connect(self._boiler_capacity_handler)
        
        # Add widgets to layout
        boilerLayout.addWidget(self.boilerConsumptionWidget)
        boilerLayout.addWidget(self.boilerTemperaturesWidget)
        boilerLayout.addWidget(self.boilerCapEnableWidget)
        boilerLayout.addWidget(self.boilerCapacityWidget)
        boilerSection.setContentLayout(boilerLayout)
        boilerSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        # Add Section to list
        parameterWidgetsList.append(boilerSection)
        
        # Finally build the stack and put it in the layout
        self.layout.addWidget(ParametersWidget(parameterWidgetsList,self),0,0,3,1)
        
    
    def __init__(self, meteo_file:str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        self.layout = QGridLayout()
        self.meteo_file = meteo_file
        self.meteo_dates,self.meteo_energies = loadMeteoCSV(meteo_file)
        
        
        self.solarPanel = Solar_Panel(0,0,100,100)
        self.dayMeteoWidget = DayMeteoWidget(self.meteo_file)
        
        mainVisuTabs = QTabWidget(self)
        mainVisuTabs.addTab(self.solarPanel,"Solar panel")
        mainVisuTabs.addTab(self.dayMeteoWidget,"Daily meteo")
        mainVisuTabs.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        self.resultsWidget = ResultsWidget()
        
        self._MakeParameterWidgets("This is the intro text")
        self.layout.addWidget(mainVisuTabs,0,1,3,3)
        self.layout.addWidget(self.resultsWidget,3,0,2,4)
        #self.layout.addWidget(QPushButton("Submit"),5,3,1,1)
        self.setLayout(self.layout)
        
        
        
        self._update_all()
        
    ##### Slots (signal handlers) #####    
    
    def _update_all(self) -> None:
        self._latitude_handler()
        self._longitude_handler()
        self._energy_received_handler()
        self._inclination_angle_handler()
        self._orientation_angle_handler()
        self._height_handler()
        self._width_handler()
        self._efficiency_handler()
        self._water_consumption_handler()
        self._water_temperature_handler()
        self._boiler_capacity_enable_handler()
        self._boiler_capacity_handler()
    
    def _latitude_handler(self) -> None:
        self.resultsWidget.energyWidget.update_latitude(self.latitudeWidget.value())
        return
    
    def _longitude_handler(self) -> None:
        return
    
    def _energy_received_handler(self) -> None:
        self.resultsWidget.energyWidget.update_received_energy(self.meteo_energies.copy())
        return
    
    def _inclination_angle_handler(self) -> None:
        self.solarPanel.update_inclination_angle(self.inclinationAngleWidget.slider.value())
        self.resultsWidget.energyWidget.update_panel_inclination(self.inclinationAngleWidget.value())
        return   
    
    def _orientation_angle_handler(self) -> None:
        self.solarPanel.update_orientation_angle(self.orientationAngleWidget.slider.value())
        self.resultsWidget.energyWidget.update_panel_orientation(self.orientationAngleWidget.value())
        return
    
    def _height_handler(self) -> None:
        self.solarPanel.update_panel_length(self.solarPanelHeightWidget.slider.value())
        self.resultsWidget.energyWidget.update_panel_height(self.solarPanelHeightWidget.value())
        return
    
    def _width_handler(self) -> None:
        self.solarPanel.update_panel_width(self.solarPanelWidthWidget.slider.value())
        self.resultsWidget.energyWidget.update_panel_width(self.solarPanelWidthWidget.value())
        return
    
    def _efficiency_handler(self) -> None:
        self.resultsWidget.energyWidget.update_efficiency(self.solarPanelEfficiencyWidget.value())
        return
    
    def _water_consumption_handler(self) -> None:
        return
    
    def _water_temperature_handler(self) -> None:
        return
    
    def _boiler_capacity_enable_handler(self) -> None:
        if self.boilerCapEnableWidget.isChecked():
            self.boilerCapacityWidget.setEnabled(True)
        else:
            self.boilerCapacityWidget.setEnabled(False)
        return
    
    def _boiler_capacity_handler(self) -> None:
        return
        
def test():
    # General PyQtGraph options
    pg.setConfigOption("background",'w')
    pg.setConfigOption("foreground",'k')
    pg.setConfigOption("antialias",True)
    
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Tab test window")
    win.setCentralWidget(TabContent("meteo.csv",win))
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    test()
        
        
        
        
        