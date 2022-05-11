import sys
import typing
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QMainWindow, QPushButton, QLabel,\
    QTabWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QRgba64
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from ParametersWidget import ParametersWidget, HBoxSlider
from Section import Section
from MeteoReader import DayMeteoWidget,MonthMeteoWidget
from ParametersWidget import OrientationWidget,HBoxSlider

meteo_file = "meteo.csv"

class Color(QWidget):
    
    def __init__(self, color:typing.Union[str,QRgba64]) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

class TabContent(QWidget):
    def _MakeParameterWidgets(self,introText:str) -> None:
        parameterWidgetsList:typing.List[QWidget] = []
        
        # Introductory text
        introTextSection = Section(title="Presentation",parent=self)
        introTextSectionLayout = QGridLayout(introTextSection.contentArea)
        introTextSectionLayout.addWidget(QLabel(introText,introTextSection.contentArea))
        introTextSection.setContentLayout(introTextSectionLayout)
        
        introTextSection.setMinimumWidth(introTextSectionLayout.itemAt(0).widget().sizeHint().width())
        parameterWidgetsList.append(introTextSection)
        
        # Meteo
        meteoSection = Section(title="Meteo",parent=self)
        meteoSectionLayout = QGridLayout(meteoSection.contentArea)
        meteoSectionLayout.addWidget(MonthMeteoWidget(meteo_file))
        meteoSection.setContentLayout(meteoSectionLayout)
        
        meteoSection.setMinimumWidth(meteoSectionLayout.itemAt(0).widget().sizeHint().width())
        parameterWidgetsList.append(meteoSection)
        
        # Solar pannel angles
        anglesSection = Section("Solar pannel angles")
        anglesLayout = QVBoxLayout(anglesSection.contentArea)
        
        verticalAngleWidget = HBoxSlider(0,90,1,"Vertical angle:","°")
        
        orientationAngleWidget = OrientationWidget(anglesSection)
        
        anglesLayout.addWidget(verticalAngleWidget)
        anglesLayout.addWidget(orientationAngleWidget)
        anglesSection.setContentLayout(anglesLayout)
        anglesSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        anglesSection.setMinimumWidth(max([verticalAngleWidget.sizeHint().width(),orientationAngleWidget.sizeHint().width()]))
        
        parameterWidgetsList.append(anglesSection)
        
        # Solar pannel dimensions
        dimSection = Section("Solar pannel dimensions")
        dimSectionLayout = QVBoxLayout(dimSection.contentArea)
        
        solarPannelWidthWidget = HBoxSlider(1,500,1,"Width:","cm")
        solarPannelHeightWidget = HBoxSlider(1,500,1,"Height:","cm")
        
        dimSectionLayout.addWidget(solarPannelWidthWidget)
        dimSectionLayout.addWidget(solarPannelHeightWidget)
        dimSection.setContentLayout(dimSectionLayout)
        dimSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
        parameterWidgetsList.append(dimSection)
        
        # Finally build the stack and put it in the layout
        self.layout.addWidget(ParametersWidget(parameterWidgetsList,self),0,0,3,1)
        
    
    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        self.layout = QGridLayout()
        
        mainVisuTabs = QTabWidget(self)
        mainVisuTabs.addTab(Color('green'),"Solar pannel")
        mainVisuTabs.addTab(DayMeteoWidget(meteo_file),"Daily meteo")
        mainVisuTabs.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        self._MakeParameterWidgets("This is the intro text")
        self.layout.addWidget(mainVisuTabs,0,1,3,3)
        self.layout.addWidget(Color('blue'),3,0,2,4)
        self.layout.addWidget(QPushButton("Submit"),5,3,1,1)
        self.setLayout(self.layout)
        
def test():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Tab test window")
    win.setCentralWidget(TabContent(win))
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    test()
        
        
        
        
        