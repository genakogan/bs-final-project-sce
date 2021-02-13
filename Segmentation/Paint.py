#GK
# importing libraries 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from pathlib import Path
import sys 
import PIL
import os
import shutil

# Constant Definition
SAVED_ICON                  = './Images/saved.png'
UNSAVED_ICON                = './Images/unsaved.png'
BACKUP_DIRECTORY_PATH       = '/Backup'
SAVED_DIFF_PATH             = 0
SAVED_SAME_PATH_DIFF_NAME   = 1
SAVED_SAME_PATH_AND_NAME    = 2

# Global Variables
savedImageFlag      = False
savedAsImageFlag    = False
savedAsPath         = SAVED_SAME_PATH_AND_NAME
savedAsFileName     = ""

# window class 
class PaintApp(QMainWindow):
    """
    Paint Class for changing imagin
    """
    
    def __init__(self, fileName,fileP): 
        
        """
            Constructor
            
        Parameters:
            self     - current object
            fileName - name of file
            fileP    - path of file
            
        Return:
            None
        """
        super().__init__() 
        
        # Set global variables
        global savedImageFlag
        global savedAsImageFlag
        global savedAsFileName
        
        # Set window icon as saved image
        self.setWindowIcon(QtGui.QIcon(SAVED_ICON)) 
        
        # setting title 
        self.setWindowTitle("Image Editor") 
       
        # Set file path
        self.filePath=fileP
       
        # Set file name 
        self.name = fileName
        
        # Reset saved file name
        savedAsFileName = ""
        
        # Reset saved image flag
        savedImageFlag = False
        savedAsImageFlag = False
        
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
        black = QAction("Split - (Black)", self) 
        
        # adding this action to the brush colors 
        b_color.addAction(black) 
        
        # adding methods to the black 
        black.triggered.connect(self.blackColor)
  
        # similarly repeating above steps for different color 
        white = QAction("Merge - (White)", self)
        b_color.addAction(white) 
        white.triggered.connect(self.whiteColor)
        
        # Create red pen
        red = QAction("Red", self) 
        b_color.addAction(red) 
        red.triggered.connect(self.redColor)
        
    # method for checking mouse cicks 
    def mousePressEvent(self, event):
        """
        Method describes a mouse press event

        Parameters:
            self  - the object
            event - mouse move event
           
        Returns:
            None.

        """ 
    
        # Set icon of the windows as unsaved image
        self.setWindowIcon(QtGui.QIcon(UNSAVED_ICON)) 
        
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
        """
        Method describes a mouse move event

        Parameters:
            self  - the object
            event - mouse move event
           
        Returns:
            None.

        """ 
        
        # If moveing the mose
        if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
            painter = QtGui.QPainter(self.imageDraw)
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            if not self.change:

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
        """
        Method describes a mouse relese event

        Parameters:
            self  - the object
            event - mouse move event
           
        Returns:
            None.

        """ 
        
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
        """
        Method gets drawing permission

        Parameters:
            self  - the object
            event - mouse move event
           
        Returns:
            None.

        """ 
        
        # Create canvas for the image
        canvasPainter = QPainter(self)
        
        # Draw the image on the canvas
        canvasPainter.drawImage(self.rect(), self.imageDraw, self.imageDraw.rect())
    
    # The function saves the image into the selected path and name
    def saveFileOperation(self, path):
        
        """
        Method can save image into the selected path and name

        Parameters:
            self  - the object
            path - selected path of image
           
        Returns:
            None.

        """ 
        
        # Set saved image flag as global varible
        global savedImageFlag
        
        # save the image into the selected path
        saveStatus = self.imageDraw.save(path)
        
        # Check if file saved
        if (saveStatus):
            # Set image has been saved
            savedImageFlag = True
            
            # Set icon as saved file
            self.setWindowIcon(QtGui.QIcon(SAVED_ICON))
            
        else:
            # Raise popup about wrong path
            messagebox.showerror(title="Error", message="Wrong path was selected try again!")
        
    # method for "save" option from file menu
    def save(self):
        """
           Method can save existing files.
        Existing files can be saved directly 
        without changing path and name of image.
        
        Parameters:
            self  - the object

        Returns:
            None.

        """
        
        # Create the path with file name to save
        strPath = self.filePath + "/" + self.name
        
        # Create path to backupd directory
        strBackupPath = self.filePath + BACKUP_DIRECTORY_PATH
        
        # Backup previous version of the file
        boolBackupExists = Path(strBackupPath).exists()
        
        # Check if backup directory not exists
        if (not boolBackupExists):
            os.mkdir(strBackupPath)
            
        # Backup the previous file before saving
        shutil.copy(strPath, strBackupPath)
        
        # Save the file
        self.saveFileOperation(strPath)
        
      
    # method for saving canvas "save as"
    def saveAs(self):
        """
           Method can save existing files.
        Existing files can be saved after
        choosing path path and name of image.
        
        Parameters:
            self  - the object
           
        Returns:
            None.

        """
        # Set global variables
        global savedAsImageFlag
        global savedAsPath
        global savedAsFileName
        
        # Set file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", self.filePath + '/' + self.name, 
                          "JPEG(*.jpg *.jpeg);;PNG(*.png);;TIF(*.tif *.tiff);;All Files(*.*) ") 
        
        # Save the image
        self.saveFileOperation(filePath)
        
        # Check if image saved successfully
        if (savedImageFlag):
            # Set saved as flag as true
            savedAsImageFlag = True
            
            # Get new file path and name
            savedAsFileName = os.path.basename(filePath)
            savedAsFilePath = os.path.dirname(filePath) 
            
            # Check if the file was saved in the same path
            if (savedAsFilePath == self.filePath):
                # Check if same file name
                if (savedAsFileName == self.name):
                    savedAsPath = SAVED_SAME_PATH_AND_NAME
                else: # Diffetent name of file
                    savedAsPath = SAVED_SAME_PATH_DIFF_NAME
            else: # Different path
                savedAsPath = SAVED_DIFF_PATH                
   
    # method for clearing every thing on canvas 
    def clear(self): 
        """
           Method  for clearing every thing on canvas
           after using brush
        
        Parameters:
            self  - the object
           
        Returns:
            None.

        """
        
        # Change the icon for unsaved image
        self.setWindowIcon(QtGui.QIcon(UNSAVED_ICON))
        
        # Check if already drawed on image
        if len(self.undoDraw) != 0:
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
        """
           The Undo command allows you to discard the most recent change.
        
        Parameters:
            self  - the object
           
        Returns:
            None.

        """
        
        self.setWindowIcon(QtGui.QIcon(UNSAVED_ICON))
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
        
        """
          The Redo command reverses the most recent change made using Undo.
        
        Parameters:
            self  - the object
           
        Returns:
            None.

        """
        
        self.setWindowIcon(QtGui.QIcon(UNSAVED_ICON))
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
        """
            changing pixel sizes in brush. 
        Size = 4
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        self.brushSize = 4
  
    def Pixel_7(self): 
        """
            changing pixel sizes in brush. 
        Size = 7
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        self.brushSize = 7
  
    def Pixel_9(self): 
        """
            changing pixel sizes in brush. 
        Size = 9
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        self.brushSize = 9
  
    def Pixel_12(self): 
        """
            changing pixel sizes in brush. 
        Size = 12
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        self.brushSize = 12
  
    # methods for changing brush color 
    def blackColor(self): 
        """
            Сhanging colour of brush. 
        Colour = black
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        self.brushColor = Qt.black 
  
    def whiteColor(self): 
        """
            Сhanging colour of brush. 
        Colour = white
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        
        self.brushColor = Qt.white 
    
    def redColor(self): 
        """
            Сhanging colour of brush. 
        Colour = red
        
        Parameters:
            self  - the object
            
        Returns:
            None

        """
        self.brushColor = Qt.red
  
paintApp = QApplication(sys.argv)