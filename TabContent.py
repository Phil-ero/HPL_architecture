import sys
import typing
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPalette, QColor, QRgba64
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from ParametersWidget import ParametersWidget, HBoxSlider
from Section import Section

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
        
    
    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        self.layout = QGridLayout()
        
        self.layout.addWidget(ParametersWidget([],self),0,0,3,1)
        self.layout.addWidget(Color('green'),0,1,3,3)
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
        
        
        
        
        