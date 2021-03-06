#!/usr/bin/env python3

import sys
import typing
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QMenuBar, QLabel
from PyQt5.QtGui import QPalette, QColor, QRgba64

from TabContent import TabContent

class Color(QWidget):
    def __init__(self,color:typing.Union[str,QRgba64]) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def _createMenuBar(self) -> None:
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        
        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")

        
    def _createTabWidget(self) -> None:
        tabWidget = QTabWidget()
        tabWidget.addTab(TabContent("meteo.csv",self),"Tab 1")
        tabWidget.addTab(TabContent("meteo.csv",self),"Tab 2")
        tabWidget.addTab(TabContent("meteo.csv",self),"Tab 3")
        self.centralWidget = tabWidget
        #self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Simulator: Generate hot water with solar panels")
        #self.resize(400, 200)
        
        #self._createMenuBar()
        self._createTabWidget()
        

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()