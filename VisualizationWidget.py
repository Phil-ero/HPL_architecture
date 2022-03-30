from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import typing

class VisualizationWidget(QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = ..., flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = ...) -> None:
        super().__init__(parent, flags)
        
        layout = QGridLayout()
        
        vueCote = QWidget()
        vueDessus = QWidget()
        vue3D = QWidget()
        
        layout.addWidget(vueCote,0,0)
        layout.addWidget(vueDessus,1,1)
        layout.addWidget(vue3D,1,0,1,2)
        
        
        