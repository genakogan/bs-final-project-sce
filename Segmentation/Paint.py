from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.Qt import Qt
 
import sys
import time
 
class Window(QMainWindow):
    def __init__(self, filename):
        super().__init__()
 
        self.title = "PyQt5 QGraphicView"
        self.top = 200
        self.left = 500
        self.width = 600
        self.height = 500
        self.lines = []
        self.filename = filename
 
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.filename)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createGraphicView()
 
        self.show()
 
 
    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)
 
        self.pen = QPen(Qt.red)
 
        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0,0,600,500)
 
        self.shapes()
        """
        #delline = self.line.pop()
        self.scene.removeItem(self.ellipse)
        del self.ellipse
        """
 
 
    def shapes(self):
        self.ellipse = self.scene.addEllipse(20,20, 200,200, self.pen, self.greenBrush)
        rect = self.scene.addRect(-100,-100, 200,200, self.pen, self.grayBrush)
        #self.line = [self.scene.addLine(20.5, 20.5, 100.5, 200.5, self.pen), self.scene.addLine(100.0, 20.0, 100.0, 30.0, self.pen)]
        """
        ## UNDO
        self.draw = []
        self.draw.append(self.scene.addLine(.....))
        self.line.append(self.draw)
        self.draw.clear()
        currentLine = self.line.pop()
        for x in currentLine:
            self.scene.removeItem(x)
          """  
        
        self.ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        self.ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
        
 
 
 
 
 
App = QApplication(sys.argv)
#window = Window()
#sys.exit(App.exec())