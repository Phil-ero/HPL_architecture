import sys
import typing
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,\
    QApplication, QMainWindow, QSlider, QLineEdit, QGridLayout, QLabel,\
    QLayout, QSizePolicy, QDial
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from superqt import QRangeSlider
from Section import Section

#################### Box for each parameter ####################

nums = "0123456789+-."

class HBoxSlider(QWidget):
    
    valueChanged = pyqtSignal()
    
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
        self.slider.setMinimumWidth(100)
        layout.addWidget(self.slider,0,1,1,2)
        
        self.textbox = QLineEdit(str(self.slider.value()),self)
        self.textbox.setMaxLength(max([len(str(maxVal)),len(str(minVal))]))
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.textbox.maxLength()+1))
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
        self.valueChanged.emit()
        
    def _TextboxUpdated(self):
        try:
            val = int(self.textbox.text())
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val))
            return
        self.slider.setValue(val)
        self.valueChanged.emit()
        
    def value(self) -> int:
        return self.slider.value()
        
class HFloatSlider(QWidget):
    
    valueChanged = pyqtSignal()
    
    def __init__(self, minVal: int, maxVal: int, decimals: int, name:str,unit:str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)
        
        self.divider = 10**decimals

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(minVal,maxVal)
        self.slider.setSingleStep(1)
        self.slider.setValue(minVal + (maxVal-minVal)//2)
        self.slider.setTickInterval(self.divider)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self._SliderUpdated)
        self.slider.setMinimumWidth(100)
        layout.addWidget(self.slider,0,1,1,2)
        
        self.textbox = QLineEdit(str(self.slider.value()/self.divider),self)
        self.textbox.setMaxLength(max([len(str(maxVal)),len(str(minVal))])+1)
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.textbox.maxLength()+1))
        self.textbox.returnPressed.connect(self._TextboxUpdated)
        layout.addWidget(self.textbox,0,3)
        
        layout.addWidget(QLabel(name+"    "),0,0,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel(str(minVal/self.divider)),1,1,1,1,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(str(maxVal/self.divider)),1,2,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(unit),0,4,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
    def _SliderUpdated(self):
        val = self.slider.value()
        self.textbox.setText(str(val/self.divider))
        self.valueChanged.emit()
        
    def _TextboxUpdated(self):
        try:
            val = int(float(self.textbox.text()) * self.divider)
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val/self.divider))
            return
        self.slider.setValue(val)
        self.valueChanged.emit()
        
    def value(self) -> float:
        return self.slider.value()/self.divider
        
class VBoxSlider(QWidget):
    
    valueChanged = pyqtSignal()
    
    def __init__(self, minVal: int, maxVal: int, stepVal: int, name:str,unit:str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)

        self.slider = QSlider(Qt.Orientation.Vertical, self)
        self.slider.setRange(minVal,maxVal)
        self.slider.setSingleStep(stepVal)
        self.slider.setValue(minVal + (maxVal-minVal)//2)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider.valueChanged.connect(self._SliderUpdated)
        self.slider.setMinimumHeight(100)
        layout.addWidget(self.slider,1,1,2,1)
        
        self.textbox = QLineEdit(str(self.slider.value()),self)
        self.textbox.setMaxLength(max([len(str(maxVal)),len(str(minVal))]))
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.textbox.maxLength()+1))
        self.textbox.returnPressed.connect(self._TextboxUpdated)
        layout.addWidget(self.textbox,0,1)
        
        layout.addWidget(QLabel(name+"    "),0,0,Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(QLabel(str(maxVal)),1,0,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(str(minVal)),2,0,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel(unit),0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
    def _SliderUpdated(self):
        val = self.slider.value()
        self.textbox.setText(str(val))
        self.valueChanged.emit()
        
    def _TextboxUpdated(self):
        try:
            val = int(self.textbox.text())
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val))
            return
        self.slider.setValue(val)
        self.valueChanged.emit()
        
    def value(self) -> int:
        return self.slider.value()
        
class VFloatSlider(QWidget):
    
    valueChanged = pyqtSignal()
    
    def __init__(self, minVal: int, maxVal: int, decimals: int, name:str,unit:str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)
        
        self.divider = 10**decimals

        self.slider = QSlider(Qt.Orientation.Vertical, self)
        self.slider.setRange(minVal,maxVal)
        self.slider.setSingleStep(1)
        self.slider.setValue(minVal + (maxVal-minVal)//2)
        self.slider.setTickInterval(self.divider)
        self.slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider.valueChanged.connect(self._SliderUpdated)
        self.slider.setMinimumHeight(100)
        layout.addWidget(self.slider,1,1,2,1)
        
        self.textbox = QLineEdit(str(self.slider.value()/self.divider),self)
        self.textbox.setMaxLength(max([len(str(maxVal)),len(str(minVal))])+1)
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.textbox.maxLength()+1))
        self.textbox.returnPressed.connect(self._TextboxUpdated)
        layout.addWidget(self.textbox,0,1)
        
        layout.addWidget(QLabel(name+"    "),0,0,Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(QLabel(str(maxVal/self.divider)),1,0,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(str(minVal/self.divider)),2,0,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel(unit),0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
    def _SliderUpdated(self):
        val = self.slider.value()
        self.textbox.setText(str(val/self.divider))
        self.valueChanged.emit()
        
    def _TextboxUpdated(self):
        try:
            val = int(float(self.textbox.text()) * self.divider)
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val/self.divider))
            return
        self.slider.setValue(val)
        self.valueChanged.emit()
        
    def value(self) -> float:
        return self.slider.value()/self.divider
    
class VRangeSlider(QWidget):
    valueChanged = pyqtSignal()
    
    def __init__(self, minVal: int, maxVal: int, stepVal: int, topName:str,bottomName:str,unit:str, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)

        self.slider = QRangeSlider(Qt.Orientation.Vertical, self)
        self.slider.setRange(minVal,maxVal)
        self.slider.setSingleStep(stepVal)
        self.slider.setValue((minVal + (maxVal-minVal)//4,minVal + 3*(maxVal-minVal)//4))
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider.valueChanged.connect(self._SliderUpdated)
        self.slider.setMinimumHeight(100)
        layout.addWidget(self.slider,1,1,2,1)
        
        self.maxTextbox = QLineEdit(str(self.slider.value()[1]),self)
        self.maxTextbox.setMaxLength(max([len(str(maxVal)),len(str(minVal))]))
        self.maxTextbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.maxTextbox.fontMetrics()
        self.maxTextbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.maxTextbox.maxLength()+1))
        self.maxTextbox.returnPressed.connect(self._MaxTextboxUpdated)
        layout.addWidget(self.maxTextbox,0,1)
        
        self.minTextbox = QLineEdit(str(self.slider.value()[0]),self)
        self.minTextbox.setMaxLength(max([len(str(maxVal)),len(str(minVal))]))
        self.minTextbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.minTextbox.fontMetrics()
        self.minTextbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.minTextbox.maxLength()+1))
        self.minTextbox.returnPressed.connect(self._MinTextboxUpdated)
        layout.addWidget(self.minTextbox,3,1)
        
        layout.addWidget(QLabel(topName+"    "),0,0,Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(QLabel(str(maxVal)),1,0,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(str(minVal)),2,0,1,1,Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(QLabel(unit),0,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(QLabel(bottomName+"    "),3,0,Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(QLabel(unit),3,2,Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        
    def _SliderUpdated(self):
        vals = self.slider.value()
        self.minTextbox.setText(str(vals[0]))
        self.maxTextbox.setText(str(vals[1]))
        self.valueChanged.emit()
        
    def _MaxTextboxUpdated(self):
        vals = self.slider.value()
        try:
            val = int(self.maxTextbox.text())
            if val <= vals[0]:
                raise ValueError
        except ValueError:
            self.maxTextbox.setText(str(vals[1]))
            return
        self.slider.setValue((vals[0],val))
        self.valueChanged.emit()
        return

    def _MinTextboxUpdated(self):
        vals = self.slider.value()
        try:
            val = int(self.minTextbox.text())
            if val >= vals[1]:
                raise ValueError
        except ValueError:
            self.minTextbox.setText(str(vals[0]))
            return
        self.slider.setValue((val,vals[1]))
        self.valueChanged.emit()
        return
    
    def value(self) -> typing.Tuple:
        return self.slider.value()
    
                
#################### Angles widget ####################

class OrientationWidget(QWidget):
    
    valueChanged = pyqtSignal()
    
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
        self.textbox.setMaxLength(len(str(-180))+1)
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(max(text_fontMetrics.widthChar(c) for c in nums)*(self.textbox.maxLength()+1))
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
        self.valueChanged.emit()
        
    def _TextboxUpdated(self):
        try:
            val = int(self.textbox.text())
        except ValueError:
            val = self.slider.value()
            self.textbox.setText(str(val))
            return
        
        self.slider.setValue(val)
        self.valueChanged.emit()
        
    def value(self) -> int:
        return self.slider.value()
    

#################### Parameters' stack ####################

class ParametersStack(QWidget):

    def _layParameters(self, paramList: typing.List[QWidget]):
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        maxWidth = 0
        for pWidget in paramList:
            layout.addWidget(pWidget)
            pWidget.setParent(self)
            pWidget.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.MinimumExpanding)
            maxWidth = max(maxWidth,pWidget.minimumWidth())
            

        self.setMinimumWidth(maxWidth)
        self.setLayout(layout)
        

    def __init__(self, paramList: typing.List[QWidget], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        self._layParameters(paramList)
        self.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.MinimumExpanding)


class ParametersWidget(QScrollArea):
    def __init__(self, paramList: typing.List[QWidget], parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(ParametersStack(paramList, self))
        self.setMinimumWidth(self.widget().minimumWidth())
        self.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.MinimumExpanding)
        

def test():
    app = QApplication(sys.argv)
    
    anglesSection = Section("Solar panel angles")
    anglesLayout = QVBoxLayout(anglesSection.contentArea)
    
    verticalAngleWidget = HBoxSlider(0,90,1,"Vertical angle:","°")
    
    orientationAngleWidget = OrientationWidget(anglesSection)
    
    anglesLayout.addWidget(verticalAngleWidget)
    anglesLayout.addWidget(orientationAngleWidget)
    anglesSection.setContentLayout(anglesLayout)
    
    anglesSection.setMinimumWidth(max([verticalAngleWidget.sizeHint().width(),orientationAngleWidget.sizeHint().width()]))
    
    dimSection = Section("Solar panel dimensions")
    dimSectionLayout = QVBoxLayout(dimSection.contentArea)
    
    solarPanelWidthWidget = HBoxSlider(1,100,1,"Width:","m")
    
    solarPanelHeightWidget = HBoxSlider(1,100,1,"Height","m")
    
    dimSectionLayout.addWidget(solarPanelWidthWidget)
    dimSectionLayout.addWidget(solarPanelHeightWidget)
    dimSection.setContentLayout(dimSectionLayout)
    
    dimSection.setMinimumWidth(max([solarPanelWidthWidget.sizeHint().width(),solarPanelHeightWidget.sizeHint().width()]))
    
    
    win = QMainWindow()
    win.setWindowTitle("Param test window")
    win.setCentralWidget(ParametersWidget([anglesSection,dimSection], win))
    #win.setCentralWidget(ParametersWidget([verticalAngleWidget,orientationAngleWidget,solarPanelHeightWidget,solarPanelWidthWidget],win))
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
    
def test_VBoxSlider():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("VBoxSlider test window")
    win.setCentralWidget(VBoxSlider(0,10,1,"Test","bar",win))
    win.show()
    sys.exit(app.exec_())
    
def test_VRangeSlider():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("VRangeSlider test window")
    win.setCentralWidget(VRangeSlider(0,10,1,"Test","bar",win))
    win.show()
    sys.exit(app.exec_())
    
def test_HFloatSlider():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("HFloatSlider test window")
    win.setCentralWidget(HFloatSlider(-1000,1000,3,"Test","bar",win))
    win.show()
    sys.exit(app.exec_())
    
def test_VFloatSlider():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("VFloatSlider test window")
    win.setCentralWidget(VFloatSlider(0,1000,2,"Test","bar",win))
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
    #test_HBoxSlider()
    #test_VBoxSlider()
    #test_VRangeSlider()
    test_HFloatSlider()
    #test_angles()
