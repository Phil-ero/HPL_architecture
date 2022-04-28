import sys
import typing
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QApplication, QMainWindow, QSlider, QLineEdit, QGridLayout, QFormLayout
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Section import Section

#################### Box for each parameter ####################

class HBoxSlider(QWidget):
    def __init__(self, minVal: int, maxVal: int, stepVal: int, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(minVal,maxVal)
        self.slider.setSingleStep(stepVal)
        self.slider.setValue(minVal + (maxVal-minVal)//2)
        self.slider.valueChanged.connect(self._SliderUpdated)
        layout.addWidget(self.slider,0,0,1,2)
        
        self.textbox = QLineEdit(str(minVal + (maxVal-minVal)//2),self)
        self.textbox.setMaxLength(len(str(maxVal)))
        text_fontMetrics = self.textbox.fontMetrics()
        self.textbox.setFixedWidth(text_fontMetrics.maxWidth()*self.textbox.maxLength())
        self.textbox.returnPressed.connect(self._TextboxUpdated)
        layout.addWidget(self.textbox,0,2)
        
        self.setLayout(layout)
        
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
        for pWidget in paramList:
            layout.addWidget(pWidget)

        self.setLayout(layout)

    def __init__(self, paramList: typing.List[QWidget], parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)

        self._layParameters(paramList)


class ParametersWidget(QScrollArea):
    def __init__(self, paramList: typing.List[QWidget], parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(ParametersStack(paramList, self))


def test():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Param test window")
    win.setCentralWidget(ParametersWidget(
        [Section("L1"), Section("L2"), Section("L3")], win))
    win.show()
    sys.exit(app.exec_())
    
def test_HBoxSlider():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("HBoxSlider test window")
    win.setCentralWidget(HBoxSlider(0,10,1,win))
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_HBoxSlider()
