# importing libraries 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
import PIL


# window class 
class Window(QMainWindow):
  
    def __init__(self): 
        super().__init__() 
        
        # setting title 
        self.setWindowTitle("Paint with PyQt5") 
        self.name="test2.tiff"
        # creating image object 
        self.image = QtGui.QImage(self.name)
        self.imageDraw = QtGui.QImage(self.name)
        #self.imageDraw.fill(QtCore.Qt.transparent)
        # setting geometry to main window 
        self.setFixedSize(self.imageDraw.size().width(), self.imageDraw.size().height()) 
      
        # variables 
        # default brush size 
        self.brushSize = 2
        # drawing flag 
        self.drawing = False
        # default color 
        self.brushColor = Qt.black 
  
        # QPoint object to tract the point 
        self.lastPoint = QPoint() 

        # eraser
        self.drawing = False
        self._clear_size = 20
        self.brushColor = QtGui.QColor(QtCore.Qt.black)
        self.lastPoint = QtCore.QPoint()
        
        # creating menu bar 
        mainMenu = self.menuBar() 
        self.change = False
        # creating file menu for save and clear action 
        fileMenu = mainMenu.addMenu("File") 
  
        # adding brush size to main menu 
        b_size = mainMenu.addMenu("Brush Size") 
  
        # adding brush color to ain menu 
        b_color = mainMenu.addMenu("Brush Color") 
  
        # creating save action 
        saveAction = QAction("Save", self) 
        # adding short cut for save action 
        saveAction.setShortcut("Ctrl+S") 
        # adding save to the file menu 
        fileMenu.addAction(saveAction) 
        # adding action to the save 
        saveAction.triggered.connect(self.save) 
  
        # creating clear action 
        clearAction = QAction("Clear", self) 
        # adding short cut to the clear action 
        clearAction.setShortcut("Ctrl+c") 
        # adding clear to the file menu 
        fileMenu.addAction(clearAction) 
        # adding action to the clear 
        clearAction.triggered.connect(self.clear) 
  
        # creating backward action
        backwardAction=QAction("Backward",self)
        backwardAction.setShortcut("Ctrl+Z")
        fileMenu.addAction(backwardAction)
        backwardAction.triggered.connect(self.backward)
        
        # araser action
        eraserAction = QtWidgets.QAction("Eraser", self)
        eraserAction.setShortcut("Ctrl+X")
        fileMenu.addAction(eraserAction)
        #eraser.addAction(eraserAction)
        eraserAction.triggered.connect(self.eraser)

  
        # creating options for brush sizes 
        # creating action for selecting pixel of 4px 
        pix_4 = QAction("4px", self) 
        # adding this action to the brush size 
        b_size.addAction(pix_4) 
        # adding method to this 
        pix_4.triggered.connect(self.Pixel_4) 
  
        # similarly repeating above steps for different sizes 
        pix_7 = QAction("7px", self) 
        b_size.addAction(pix_7) 
        pix_7.triggered.connect(self.Pixel_7) 
  
        pix_9 = QAction("9px", self) 
        b_size.addAction(pix_9) 
        pix_9.triggered.connect(self.Pixel_9) 
  
        pix_12 = QAction("12px", self) 
        b_size.addAction(pix_12) 
        pix_12.triggered.connect(self.Pixel_12) 
  
        # creating options for brush color 
        # creating action for black color 
        black = QAction("Black", self) 
        # adding this action to the brush colors 
        b_color.addAction(black) 
        # adding methods to the black 
        black.triggered.connect(self.blackColor) 
  
        # similarly repeating above steps for different color 
        white = QAction("White", self) 
        b_color.addAction(white) 
        white.triggered.connect(self.whiteColor) 
  
        red = QAction("Red", self) 
        b_color.addAction(red) 
        red.triggered.connect(self.redColor) 
        
        
    # method for checking mouse cicks 
    def mousePressEvent(self, event): 
        
        # if left mouse button is pressed 
        if event.button() == Qt.LeftButton:             
            # make drawing flag true 
            self.drawing = True
            # make last point to the point of cursor 
            self.lastPoint = event.pos()
        
        
    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            painter = QtGui.QPainter(self.imageDraw)
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            if self.change:
                r = QtCore.QRect(QtCore.QPoint(), self._clear_size*QtCore.QSize())
                r.moveCenter(event.pos())
                painter.save()
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
                painter.eraseRect(r)
                painter.restore()
            else:
                painter.drawLine(self.lastPoint, event.pos())
            painter.end()
            self.lastPoint = event.pos()
            self.update()
          
    # method for mouse left button release 
    def mouseReleaseEvent(self, event): 
  
        if event.button() == QtCore.Qt.LeftButton: 
            # make drawing flag false 
            self.drawing = False
       
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(),self.image, self.image.rect())
        canvasPainter.drawImage(self.rect(), self.imageDraw, self.imageDraw.rect())

    # eraser method
    def eraser(self):
        self.change = not self.change
        if self.change:
            pixmap = QtGui.QPixmap(QtCore.QSize(1, 1)*self._clear_size)
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.drawRect(pixmap.rect())
            painter.end()
            cursor = QtGui.QCursor(pixmap)
            QtWidgets.QApplication.setOverrideCursor(cursor)
        else:
            QtWidgets.QApplication.restoreOverrideCursor()  
    # method for saving canvas 
    def save(self): 
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", self.name, 
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ") 
  
        if filePath == "": 
            return
        self.imageDraw.save(filePath) 
  
    # method for clearing every thing on canvas 
    def clear(self): 
        
        # make the whole canvas white 
        #self.image = QImage(self.name) 
        self.imageDraw = QtGui.QImage(self.name)
        # update 
        self.update() 
   # Undo method
    def backward(self):
        self.image = QImage(self.name)
        self.update()
        
    # methods for changing pixel sizes 
    def Pixel_4(self): 
        self.brushSize = 4
  
    def Pixel_7(self): 
        self.brushSize = 7
  
    def Pixel_9(self): 
        self.brushSize = 9
  
    def Pixel_12(self): 
        self.brushSize = 12
  
    # methods for changing brush color 
    def blackColor(self): 
        self.brushColor = Qt.black 
  
    def whiteColor(self): 
        self.brushColor = Qt.white 
    
    def redColor(self): 
        self.brushColor = Qt.red 
  
# create pyqt5 app 
App = QApplication(sys.argv) 
 
# create the instance of our Window 
window = Window() 
  
# showing the wwindow 
window.show() 

# start the app 
sys.exit(App.exec())