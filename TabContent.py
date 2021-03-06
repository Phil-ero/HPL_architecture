import sys, os
import typing
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QMainWindow, QPushButton, QLabel,\
    QTabWidget, QVBoxLayout, QSizePolicy, QCheckBox, QFileDialog, QComboBox
from PyQt5.QtCore import Qt
import pyqtgraph as pg

from ParametersWidget import ParametersWidget, HBoxSlider, VBoxSlider, VRangeSlider, HFloatSlider, VFloatSlider,\
                            OrientationWidget,HBoxSlider
from Section import Section
from MeteoReader import DayMeteoWidget,MonthMeteoWidget, loadMeteoCSV
from Solarvizu import Solar_Panel
from ResultsWidget import ResultsWidget
from datetime import timedelta

UTC_timezones:typing.List[typing.Tuple[str,timedelta]] = [
    ("UTC -12:00", timedelta(hours=12,minutes=0)),
    ("UTC -11:00", timedelta(hours=11,minutes=0)),
    ("UTC -10:00", timedelta(hours=10,minutes=0)),
    ("UTC -09:30", timedelta(hours=9,minutes=30)),
    ("UTC -09:00", timedelta(hours=9,minutes=0)),
    ("UTC -08:00", timedelta(hours=8,minutes=0)),
    ("UTC -07:00", timedelta(hours=7,minutes=0)),
    ("UTC -06:00", timedelta(hours=6,minutes=0)),
    ("UTC -05:00", timedelta(hours=5,minutes=0)),
    ("UTC -04:00", timedelta(hours=4,minutes=0)),
    ("UTC -03:30", timedelta(hours=3,minutes=30)),
    ("UTC -03:00", timedelta(hours=3,minutes=0)),
    ("UTC -02:00", timedelta(hours=1,minutes=0)),
    ("UTC -01:00", timedelta(hours=2,minutes=0)),
    ("UTC ±00:00", timedelta(hours=00,minutes=0)),
    ("UTC +01:00", -timedelta(hours=1,minutes=0)),
    ("UTC +02:00", -timedelta(hours=2,minutes=0)),
    ("UTC +03:00", -timedelta(hours=3,minutes=0)),
    ("UTC +03:30", -timedelta(hours=3,minutes=30)),
    ("UTC +04:00", -timedelta(hours=4,minutes=0)),
    ("UTC +04:30", -timedelta(hours=4,minutes=30)),
    ("UTC +05:00", -timedelta(hours=5,minutes=0)),
    ("UTC +05:30", -timedelta(hours=5,minutes=30)),
    ("UTC +05:45", -timedelta(hours=5,minutes=45)),
    ("UTC +06:00", -timedelta(hours=6,minutes=0)),
    ("UTC +06:30", -timedelta(hours=6,minutes=30)),
    ("UTC +07:00", -timedelta(hours=7,minutes=0)),
    ("UTC +08:00", -timedelta(hours=8,minutes=0)),
    ("UTC +08:45", -timedelta(hours=8,minutes=45)),
    ("UTC +09:00", -timedelta(hours=9,minutes=0)),
    ("UTC +09:30", -timedelta(hours=9,minutes=30)),
    ("UTC +10:00", -timedelta(hours=10,minutes=0)),
    ("UTC +10:30", -timedelta(hours=10,minutes=30)),
    ("UTC +11:00", -timedelta(hours=11,minutes=0)),
    ("UTC +12:00", -timedelta(hours=12,minutes=0)),
    ("UTC +12:45", -timedelta(hours=12,minutes=45)),
    ("UTC +13:00", -timedelta(hours=13,minutes=0)),
    ("UTC +14:00", -timedelta(hours=14,minutes=0)),
]

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
        self.backToGenevaButton = QPushButton("Back to Geneva !",parent=localisationSection)
        self.backToGenevaButton.clicked.connect(self._back_to_geneva)
        self.latitudeWidget = VFloatSlider(-90000,90000,3,"Latitude","°")
        self.latitudeWidget.slider.setValue(46204)
        self.latitudeWidget.valueChanged.connect(self._latitude_handler)
        self.longitudeWidget = HFloatSlider(-180000,180000,3,"Longitude","°")
        self.longitudeWidget.slider.setValue(6143)
        self.longitudeWidget.valueChanged.connect(self._longitude_handler)
        self.timezoneWidget = QComboBox(self)
        for s,dt in UTC_timezones:
            self.timezoneWidget.addItem(s,dt)
            
        self.timezoneWidget.setEditable(False)
        self.timezoneWidget.setCurrentIndex(16) #UTC +02:00; Geneva 
        self.timezoneWidget.currentIndexChanged.connect(self._timezone_handler)
    
        
        self.timezoneLabel = QLabel("UTC Timezone: ")
        self.timezoneLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        
        # Layout
        localisationLayout.addWidget(self.backToGenevaButton,0,0,1,2)
        localisationLayout.addWidget(self.latitudeWidget,2,0,2,1)
        localisationLayout.addWidget(self.longitudeWidget,1,0,1,2)
        localisationLayout.addWidget(self.timezoneLabel,4,0)
        localisationLayout.addWidget(self.timezoneWidget,4,1)
        localisationSection.setContentLayout(localisationLayout)
        localisationSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        parameterWidgetsList.append(localisationSection)
        
        
        ## Meteo
        meteoSection = Section(title="Meteo",parent=self)
        meteoSectionLayout = QGridLayout(meteoSection.contentArea)
        self.meteoWidget = MonthMeteoWidget(self.meteo_file)
        meteoSectionLayout.addWidget(self.meteoWidget,0,0,2,2)
        
        self.meteoFileLabel = QLabel(f"Current file: {os.path.basename(self.meteo_file)}")
        meteoFileButton = QPushButton("Select new meteo file", self)
        
        meteoFileButton.clicked.connect(self._getfile)
        
        meteoSectionLayout.addWidget(meteoFileButton,2,0,1,1)
        meteoSectionLayout.addWidget(self.meteoFileLabel,2,1,1,1)
        
        
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
        self.orientationAngleWidget.slider.setValue(145)
        self.orientationAngleWidget.valueChanged.connect(self._orientation_angle_handler)
        
        self.solarPanelWidthWidget = HBoxSlider(1,10000,1,"Width:","cm")
        self.solarPanelWidthWidget.slider.setValue(3000)
        self.solarPanelWidthWidget.valueChanged.connect(self._width_handler)
        
        self.solarPanelHeightWidget = HBoxSlider(1,10000,1,"Height:","cm")
        self.solarPanelHeightWidget.slider.setValue(1000)
        self.solarPanelHeightWidget.valueChanged.connect(self._height_handler)
        
        self.solarPanelSurfaceWidget = QLabel("\t Solar panel's surface: 3 m²")
        self.solarPanelSurfaceWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.solarPanelEfficiencyWidget = HBoxSlider(1,100,1,"Efficiency",'%')
        self.solarPanelEfficiencyWidget.valueChanged.connect(self._efficiency_handler)
        
        # Add widgets to layout
        solarPanelLayout.addWidget(self.inclinationAngleWidget)
        solarPanelLayout.addWidget(self.orientationAngleWidget)
        solarPanelLayout.addWidget(self.solarPanelWidthWidget)
        solarPanelLayout.addWidget(self.solarPanelHeightWidget)
        solarPanelLayout.addWidget(self.solarPanelSurfaceWidget)
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
        self.boilerConsumptionWidget.slider.setValue(80)
        self.boilerConsumptionWidget.valueChanged.connect(self._water_consumption_handler)
        
        self.boilerTemperaturesWidget = VRangeSlider(0,100,1,"Water output temperature", "Water input temperature","°C")
        self.boilerTemperaturesWidget.slider.setValue((10,35))
        self.boilerTemperaturesWidget.valueChanged.connect(self._water_temperature_handler)
        
        self.boilerCapEnableWidget = QCheckBox("Hot water storage tank")
        self.boilerCapEnableWidget.setChecked(False)
        self.boilerCapEnableWidget.toggled.connect(self._boiler_enable_handler)
        
        self.boilerCapacityWidget = HBoxSlider(1,10000,1,"Tank's capacity", "L")
        self.boilerCapacityWidget.setDisabled(True)
        self.boilerCapacityWidget.valueChanged.connect(self._boiler_handler)
        
        self.boilerRetainabilityWidget = HBoxSlider(1,100,1,"Tank's retainability", "%")
        self.boilerRetainabilityWidget.setDisabled(True)
        self.boilerRetainabilityWidget.valueChanged.connect(self._boiler_handler)
        
        self.boilerRetainabilityLabel = QLabel("Tank's retainability: hot water's proportion in the tank kept from a day to the next")
        
        # Add widgets to layout
        boilerLayout.addWidget(self.boilerConsumptionWidget)
        boilerLayout.addWidget(self.boilerTemperaturesWidget)
        boilerLayout.addWidget(self.boilerCapEnableWidget)
        boilerLayout.addWidget(self.boilerCapacityWidget)
        boilerLayout.addWidget(self.boilerRetainabilityWidget)
        boilerLayout.addWidget(self.boilerRetainabilityLabel)
        boilerSection.setContentLayout(boilerLayout)
        boilerSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        # Add Section to list
        parameterWidgetsList.append(boilerSection)
        
        # Finally build the stack and put it in the layout
        self.layout.addWidget(ParametersWidget(parameterWidgetsList,self),0,0,1,1)
        
    
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
        self.layout.addWidget(mainVisuTabs,0,1,1,2)
        self.layout.addWidget(self.resultsWidget,1,0,2,4)
        #self.layout.addWidget(QPushButton("Submit"),5,3,1,1)
        self.setLayout(self.layout)
        
        
        
        self._update_all()
        
    ##### Slots (signal handlers) #####    
    
    def _getfile(self) -> None:
        returned = QFileDialog.getOpenFileName(self,"Select meteo file",".","CSV file (*.csv)")
        if returned:
            self.meteo_file = returned[0]
        
        #print(returned)
        self.meteoFileLabel.setText(f"Current file: {os.path.basename(self.meteo_file)}")
        self.meteo_dates,self.meteo_energies = loadMeteoCSV(self.meteo_file)
        
        self.dayMeteoWidget.update(self.meteo_file)
        self.meteoWidget.update(self.meteo_file)
        self._energy_received_handler()
        
    
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
        self._boiler_enable_handler()
        self._boiler_handler()
    
    def _back_to_geneva(self) -> None:
        self.latitudeWidget.slider.setValue(46204)
        self.longitudeWidget.slider.setValue(6143)
        self.timezoneWidget.setCurrentIndex(16)
        self._latitude_handler()
        self._longitude_handler()
    
    def _latitude_handler(self) -> None:
        self.resultsWidget.energyWidget.update_latitude(self.latitudeWidget.value())
        return
    
    def _longitude_handler(self) -> None:
        self.resultsWidget.energyWidget.update_longitude(self.longitudeWidget.value())
        return
    
    def _timezone_handler(self) -> None:
        self.resultsWidget.energyWidget.update_timedelta(self.timezoneWidget.currentData())
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
        self._surface_handler()
        return
    
    def _width_handler(self) -> None:
        self.solarPanel.update_panel_width(self.solarPanelWidthWidget.slider.value())
        self.resultsWidget.energyWidget.update_panel_width(self.solarPanelWidthWidget.value())
        self._surface_handler()
        return
    
    def _surface_handler(self) -> None:
        # Get height and width in cm, convert to m
        height = self.solarPanelHeightWidget.value()/100
        width = self.solarPanelWidthWidget.value()/100
        
        self.solarPanelSurfaceWidget.setText(f"\t Solar panel's surface: {height*width:.2} m²")
    
    def _efficiency_handler(self) -> None:
        self.resultsWidget.energyWidget.update_efficiency(self.solarPanelEfficiencyWidget.value()/100)
        return
    
    def _water_consumption_handler(self) -> None:
        self.resultsWidget.satisfactionWidget.update_volume_wanted(self.boilerConsumptionWidget.value())
        return
    
    def _water_temperature_handler(self) -> None:
        self.resultsWidget.satisfactionWidget.update_temperatures(self.boilerTemperaturesWidget.value())
        return
    
    def _boiler_enable_handler(self) -> None:
        if self.boilerCapEnableWidget.isChecked():
            self.boilerCapacityWidget.setEnabled(True)
            self.boilerRetainabilityWidget.setEnabled(True)
            self.resultsWidget.satisfactionWidget.update_water_tank(True,self.boilerCapacityWidget.value(),self.boilerRetainabilityWidget.value())
        else:
            self.boilerCapacityWidget.setEnabled(False)
            self.boilerRetainabilityWidget.setEnabled(False)
            self.resultsWidget.satisfactionWidget.update_water_tank(False,self.boilerCapacityWidget.value(),self.boilerRetainabilityWidget.value())
        return
    
    def _boiler_handler(self) -> None:
        self.resultsWidget.satisfactionWidget.update_water_tank(self.boilerCapEnableWidget.isChecked(),self.boilerCapacityWidget.value(), self.boilerRetainabilityWidget.value()/100)
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
        
        
        
        
        