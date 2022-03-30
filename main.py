#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGroupBox, QBoxLayout
from PyQt5.QtCore import Qt

import ParametersWidget, VisualizationWidget, ResultsWidget

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        mainWidget = QWidget()

        layout = QBoxLayout(QBoxLayout.LeftToRight)

        self.setWindowTitle("Test App")
        leftFrame = QGroupBox("Parameters", self)
        leftFrame.setAlignment(Qt.AlignLeft)
        
        midFrame = QGroupBox("Visualisation",self)
        midFrame.setAlignment(Qt.AlignCenter)
        
        rightFrame = QGroupBox("Results",self)
        rightFrame.setAlignment(Qt.AlignRight)
        
        layout.addWidget(leftFrame)
        layout.addWidget(midFrame)
        layout.addWidget(rightFrame)
        
        mainWidget.setLayout(layout)
        
        self.setCentralWidget(mainWidget)
        

window = MainWindow()
window.show()

# Start the event loop.
app.exec()