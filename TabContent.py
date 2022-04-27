import sys
import typing
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QMainWindow
from PyQt5.QtGui import QPalette, QColor, QRgba64
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt

class Color(QWidget):
    
    def __init__(self, color:typing.Union[str,QRgba64]) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class TabContent(QWidget):
    def __init__(self, parent: typing.Optional['QWidget'] = None) -> None:
        super().__init__(parent)
        
        layout = QGridLayout()
        
        layout.addWidget(Color('red'),0,0,3,1)
        layout.addWidget(Color('green'),0,1,3,3)
        layout.addWidget(Color('blue'),3,0,2,4)
        self.setLayout(layout)
        
def test():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Tab test window")
    win.setCentralWidget(TabContent(win))
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    test()
        
        
        
        
        