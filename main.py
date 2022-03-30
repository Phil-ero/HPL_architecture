#!/usr/bin/env python3

import sys
from unittest import result
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGroupBox, QBoxLayout, QGridLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

import ParametersWidget, VisualizationWidget, ResultsWidget

app = QApplication(sys.argv)

class Color(QWidget):
    
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget = QWidget()

        #layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout = QGridLayout()

        self.setWindowTitle("Test App")
        paramFrame = QGroupBox("Parameters", self)
        paramFrame.setAlignment(Qt.AlignCenter)
        
        paramlayout = QBoxLayout(QBoxLayout.TopToBottom)
        paramlayout.addWidget(QLabel("Param1"))
        paramlayout.addWidget(QSlider(Qt.Horizontal))
        paramlayout.addWidget(QLabel("Param2"))
        paramlayout.addWidget(QSlider(Qt.Horizontal))
        paramlayout.addWidget(QLabel("Param3"))
        paramlayout.addWidget(QSlider(Qt.Horizontal))
        
        paramFrame.setLayout(paramlayout)
        
        visFrame = QGroupBox("Visualisation",self)
        visFrame.setAlignment(Qt.AlignCenter)
        
        vislayout = QBoxLayout(QBoxLayout.TopToBottom)
        vislayout.addWidget(Color(QColor(255,0,0)))
        
        visFrame.setLayout(vislayout)
        
        resultsFrame = QGroupBox("Results",self)
        resultsFrame.setAlignment(Qt.AlignCenter)
        
        resulstlayout = QBoxLayout(QBoxLayout.LeftToRight)
        resulstlayout.addWidget(Color(QColor(0,0,255)))
        resulstlayout.addWidget(Color(QColor(255,255,255)))
        resulstlayout.addWidget(Color(QColor(255,0,0)))
        
        resultsFrame.setLayout(resulstlayout)
        
        
        layout.addWidget(paramFrame,0,0)
        layout.addWidget(visFrame,0,1)
        layout.addWidget(resultsFrame,1,0,1,2)
        
        
        mainWidget.setLayout(layout)
        
        self.setCentralWidget(mainWidget)

        

window = MainWindow()
window.show()

# Start the event loop.
app.exec()