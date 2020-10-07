from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QPixmap
from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
 
import PIL.ImageQt as imqt
import sys
import time
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.title = "PyQt5 QGraphicView"
        self.top = 200
        self.left = 500
        self.width = 600
        self.height = 500
        self.lines = []
 
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createGraphicView()   
 
        #self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        
        self.show()
        self.save_image()
 
 
    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)
 
        self.pen = QPen(Qt.red)
 
        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0,0,600,500)
 
        # Display image
        self.imgQ = imqt.ImageQt("crop.jpg")  # we need to hold reference to imgQ, or it will crash
        pixMap = QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
 
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
        #self.ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        #rect.setFlag(QGraphicsItem.ItemIsMovable)
        #self.ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
        
 
    def _save_image(self):

        # Get region of scene to capture from somewhere.
        area = get_QRect_to_capture_from_somewhere()
    
        # Create a QImage to render to and fix up a QPainter for it.
        image = QImage(area.size(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)
    
        # Render the region of interest to the QImage.
        self.scene.render(painter, image.rect(), area)
        painter.end()
    
        # Save the image to a file.
        image.save("capture.png")
 
 
 
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())