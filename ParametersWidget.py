import sys
import typing
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,\
    QApplication, QMainWindow, QSlider, QLineEdit, QGridLayout, QLabel,\
    QLayout, QSizePolicy, QDial
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Section import Section

#################### Box for each parameter ####################

class HBoxSlider(QWidget):
    def __init__(self, minVal: int, maxVal: int, stepVal: int, name:str,unit:str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(minVal,maxVal)
        self.slider.setSingleStep(stepVal)
        self.slider.setValue(minVal + (maxVal-minVal)//2)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self._SliderUpdated)
        self.slider.setMinimumWidth(200)
        layout.addWidget(self.slider,0,1,1,2)
        
        self.textbox = QLineEdit(str(self.slider.value()),self)
        self.textbox.setMaxLength(len(str(maxVal)))
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(text_fontMetrics.maxWidth()*self.textbox.maxLength())
        self.textbox.returnPressed.connect(self._TextboxUpdated)
        layout.addWidget(self.textbox,0,3)
        
        layout.addWidget(QLabel(name+"    "),0,0,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel(str(minVal)),1,1,1,1,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(str(maxVal)),1,2,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(unit),0,4,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
    def _SliderUpdated(self):
        val = self.slider.value()
        self.textbox.setText(str(val))
        
    def _TextboxUpdated(self):
        try:
            val = int(self.textbox.text())
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val))
            return
        
        self.slider.setValue(val)
                
#################### Angles widget ####################

class OrientationWidget(QWidget):
    def __init__(self,parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)

        self.slider = QDial(self)
        self.slider.setRange(-180,180)
        self.slider.setSingleStep(1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self._SliderUpdated)
        self.slider.setWrapping(True)
        self.slider.setNotchesVisible(True)
        layout.addWidget(self.slider,1,2,Qt.AlignmentFlag.AlignCenter)
        
        
        self.textbox = QLineEdit(str(self.slider.value()),self)
        self.textbox.setMaxLength(len(str(-180)))
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(text_fontMetrics.maxWidth()*self.textbox.maxLength()//2)
        self.textbox.returnPressed.connect(self._TextboxUpdated)
        layout.addWidget(self.textbox,1,4)
        
        layout.addWidget(QLabel("Orientation:    "),1,0,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("W"),1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(QLabel("N"),0,2,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel("E    "),1,3,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(QLabel("S"),2,2,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel("°"),1,5,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
    def _SliderUpdated(self):
        val = self.slider.value()
        self.textbox.setText(str(val))
        
    def _TextboxUpdated(self):
        try:
            val = int(self.textbox.text())
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val))
            return
        
        self.slider.setValue(val)
        
        
        
    

#################### Parameters' stack ####################

class ParametersStack(QWidget):

    def _layParameters(self, paramList: typing.List[QWidget]):
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        for pWidget in paramList:
            layout.addWidget(pWidget)

        self.setLayout(layout)

    def __init__(self, paramList: typing.List[QWidget], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        self._layParameters(paramList)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)


class ParametersWidget(QScrollArea):
    def __init__(self, paramList: typing.List[QWidget], parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(ParametersStack(paramList, self))
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        

def test():
    app = QApplication(sys.argv)
    
    anglesSection = Section("Solar pannel angles")
    anglesLayout = QVBoxLayout(anglesSection.contentArea)
    
    verticalAngleWidget = HBoxSlider(0,90,1,"Vertical angle:","°",verticalAngleWidget)
    
    
    orientationAngleWidget = OrientationWidget(anglesSection)
    
    anglesLayout.addWidget(verticalAngleWidget)
    anglesLayout.addWidget(orientationAngleWidget)
    anglesSection.setContentLayout(anglesLayout)
    anglesSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
    
    anglesSection.setMinimumWidth(max([verticalAngleWidget.sizeHint().width(),orientationAngleWidget.sizeHint().width()]))
    
    dimSection = Section("Solar pannel dimensions")
    dimSectionLayout = QVBoxLayout(dimSection.contentArea)
    
    solarPannelWidthWidget = HBoxSlider(1,100,1,"Width:","m",solarPannelWidthWidget)
    solarPannelWidthLayout = QHBoxLayout(solarPannelWidthWidget)
    solarPannelWidthLayout.addWidget(QLabel("Width"),alignment=Qt.AlignmentFlag.AlignLeft)
    solarPannelWidthLayout.addWidget()
    solarPannelWidthLayout.addWidget(QLabel("m"),alignment=Qt.AlignmentFlag.AlignLeft)
    
    solarPannelHeightWidget = QWidget(dimSection)
    solarPannelHeightLayout = QHBoxLayout(solarPannelHeightWidget)
    solarPannelHeightLayout.addWidget(QLabel("Height"),alignment=Qt.AlignmentFlag.AlignLeft)
    solarPannelHeightLayout.addWidget(HBoxSlider(1,100,1,solarPannelHeightWidget))
    solarPannelHeightLayout.addWidget(QLabel("m"),alignment=Qt.AlignmentFlag.AlignLeft)
    
    dimSectionLayout.addWidget(solarPannelWidthWidget)
    dimSectionLayout.addWidget(solarPannelHeightWidget)
    dimSection.setContentLayout(dimSectionLayout)
    dimSection.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
    
    dimSection.setMinimumWidth(max([solarPannelHeightLayout.sizeHint().width(),solarPannelWidthLayout.sizeHint().width()]))
    
    
    win = QMainWindow()
    win.setWindowTitle("Param test window")
    win.setCentralWidget(ParametersWidget([anglesSection,dimSection], win))
    #win.setCentralWidget(ParametersWidget([verticalAngleWidget,orientationAngleWidget,solarPannelHeightWidget,solarPannelWidthWidget],win))
    #win.setCentralWidget(anglesSection)
    win.show()
    sys.exit(app.exec_())
    
def test_HBoxSlider():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("HBoxSlider test window")
    win.setCentralWidget(HBoxSlider(0,10,1,"Test","bar",win))
    win.show()
    sys.exit(app.exec_())
    
def test_angles():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("OrientationWidget test window")
    win.setCentralWidget(OrientationWidget(win))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    #test()
    test_HBoxSlider()
    #test_angles()
