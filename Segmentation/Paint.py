#GK
# importing libraries 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
import PIL

# Constant Definition
GREEN_ICON  = './Images/green.png'
RED_ICON    = './Images/red.png'


# window class 
class Window(QMainWindow):
    
    def __init__(self, fileName,fileP): 
        super().__init__() 
        self.setWindowIcon(QtGui.QIcon(GREEN_ICON)) 
        
        # setting title 
        self.setWindowTitle("Image Editor") 
       
        # Set file path
        self.filePath=fileP
       
        # Set file name 
        self.name = fileName
        #self.fame = fileName
      
        # creating image object that we will edit
        self.imageDraw = QtGui.QImage(self.filePath + '/' + self.name)
        
        # Array of undo and redo drawings
        self.undoDraw = []
        self.redoDraw = []

        # Get image dimensions
        width, height = self.imageDraw.size().width(), self.imageDraw.size().height()
        
        # setting the minimum size of the window as the image size
        self.setMinimumSize(width, height) 
        
        # Prepare varible for scale window in order to be able resize the window and draw
        self.scale_x = 0
        self.scale_y = 0
      
        # variables 
        # default brush size 
        self.brushSize = 2
        
        # drawing flag 
        self.drawing = False
        
        # default color 
        self.brushColor = Qt.black 
  
        # QPoint object to tract the point 
        self.lastPoint = QPoint() 
        
        # creating menu bar 
        mainMenu = self.menuBar() 
        self.change = False
         
       
        
        # creating file menu for save and clear action 
        fileMenu = mainMenu.addMenu("File")
       
        # creating edit menu for undo and redo
        editMenu = mainMenu.addMenu("Edit") 
  
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
        
        saveAsAction = QAction("Save As", self) 
        # adding short cut for save action 
        saveAsAction.setShortcut("Ctrl+Shift+S")
        # adding save to the file menu 
        fileMenu.addAction(saveAsAction) 
        
        # adding action to the save 
        saveAsAction.triggered.connect(self.saveAs) 
  
        # creating clear action 
        clearAction = QAction("Clear", self) 
        # adding short cut to the clear action 
        clearAction.setShortcut("Ctrl+c") 
        # adding clear to the file menu 
        fileMenu.addAction(clearAction) 
        # adding action to the clear 
        clearAction.triggered.connect(self.clear) 

        # creating exit action     
        exitAct = QAction('Exit', self)
        # adding short cut to the exit action
        exitAct.setShortcut('Ctrl+Q')
        # adding exit to the file menu 
        fileMenu.addAction(exitAct)
        # adding action to the exit 
        exitAct.triggered.connect(self.close)
        

  
        # creating undo action
        self.undoAction=QAction("Undo",self)
        self.undoAction.setShortcut("Ctrl+Z")
        editMenu.addAction(self.undoAction)
        self.undoAction.triggered.connect(self.undo)
        self.undoAction.setDisabled(True)
        
        # creating redo action
        self.redoAction=QAction("Redo",self)
        self.redoAction.setShortcut("Ctrl+Y")
        editMenu.addAction(self.redoAction)
        self.redoAction.triggered.connect(self.redo)
        self.redoAction.setDisabled(True)

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
        
        # Create red pen
        red = QAction("Red", self) 
        b_color.addAction(red) 
        red.triggered.connect(self.redColor) 
        
        
        
        
    # method for checking mouse cicks 
    def mousePressEvent(self, event): 
        self.setWindowIcon(QtGui.QIcon(RED_ICON)) 
        # Get windows size in order to scale drawing
        winSize = self.size()
        imgSize = self.imageDraw.size()
        
        # Prepare the scale ratio for the screen
        self.scale_x, self.scale_y = winSize.width() / imgSize.width() , winSize.height() / imgSize.height() 
        
        # if left mouse button is pressed 
        if event.button() == Qt.LeftButton:
            # Backup previous image
            self.undoDraw.append(self.imageDraw.copy())
             
            # make drawing flag true 
            self.drawing = True
            
            # Create scaled point according to screen size
            newX = event.x() / self.scale_x
            newY = event.y() / self.scale_y
            
            # make last point to the point of cursor
            scaledPoint = QPoint(newX, newY)
            
            # Scale the point according to screen size
            self.lastPoint = scaledPoint
        
        
    def mouseMoveEvent(self, event):
        # If moveing the mose
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            painter = QtGui.QPainter(self.imageDraw)
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            if not self.change:
                """r = QtCore.QRect(QtCore.QPoint(), self._clear_size*QtCore.QSize())
                r.moveCenter(event.pos())
                painter.save()
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
                painter.eraseRect(r)
                painter.restore()"""
            #else:
                # Scale the point according to windows size
                newX = event.x() / self.scale_x
                newY = event.y() / self.scale_y
                
                # Create scaled current point
                scaledPoint = QPoint(newX, newY)
                
                # Print the line between previous and current point
                painter.drawLine(self.lastPoint, scaledPoint)
            
            # End drawing
            painter.end()
            
            # Save last scaled point
            self.lastPoint = scaledPoint
            
            # Update the screen
            self.update()
          
    # method for mouse left button release 
    def mouseReleaseEvent(self, event): 
        
        # Check if button was released the drwaing stopped
        if event.button() == QtCore.Qt.LeftButton: 
            # make drawing flag false 
            self.drawing = False
            
            # Enable the undo menu
            self.undoAction.setDisabled(False)
            
            # Clear the redo list because new drawing created
            self.redoDraw.clear()
            
            # Disable redo menu
            self.redoAction.setDisabled(True)
       
    def paintEvent(self, event):
        # Create canvas for the image
        canvasPainter = QPainter(self)
        
        # Draw the image on the canvas
        canvasPainter.drawImage(self.rect(), self.imageDraw, self.imageDraw.rect())
        
    # method for saving canvas "save"
    def save(self):  
        # Set icon as saved file
        self.setWindowIcon(QtGui.QIcon(GREEN_ICON))
        
        # Path is correct save the image to the path
        self.imageDraw.save(self.filePath + "/" + self.name) 
      
    # method for saving canvas "save as"
    def saveAs(self):
        self.setWindowIcon(QtGui.QIcon(GREEN_ICON))
        # Set file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", self.filePath + '/' + self.name, 
                          "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ") 
       
        # If path is empty then wrong path - don't save the image
        if ( filePath == "" ): 
            return
        
        # Path is correct save the image to the path
        self.imageDraw.save(filePath)
   
    # method for clearing every thing on canvas 
    def clear(self): 
        
        # clear all changes on the image
        self.imageDraw = QtGui.QImage(self.undoDraw[0])
        
        # Clear undo and redo arrays
        self.undoDraw.clear()
        self.redoDraw.clear()
        
        # Diable undo and redo menu
        self.undoAction.setDisabled(True)
        self.redoAction.setDisabled(True)
        
        # update 
        self.update()
        
    # Undo method
    def undo(self):
        self.setWindowIcon(QtGui.QIcon(RED_ICON))
        # Backup current version for redo
        self.redoDraw.append(self.imageDraw.copy())
        
        # Copy previus version of the image
        self.imageDraw = self.undoDraw.pop().copy()
        
        # Check if undo list empty disable the button
        if(len(self.undoDraw) == 0):
            # Disable undo menu
            self.undoAction.setDisabled(True)
            
        # Enable redo menu
        self.redoAction.setDisabled(False)
        
        # Update the screen
        self.update()
        
    # Redo method
    def redo(self):
        self.setWindowIcon(QtGui.QIcon(RED_ICON))
        # Backup current version for undo
        self.undoDraw.append(self.imageDraw.copy())
        
        # Copy last version from redoof the image
        self.imageDraw = self.redoDraw.pop().copy()
        
        # Check if redo list empty disable the button
        if(len(self.redoDraw) == 0):
            # Disable undo menu
            self.redoAction.setDisabled(True)
            
        # Enable undo menu
        self.undoAction.setDisabled(False)
        
        # Update the screen
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
  
App = QApplication(sys.argv)
