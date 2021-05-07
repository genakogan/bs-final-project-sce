import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
import os
from pathlib import Path
from shutil import copytree

# Constant Definition
ACCEPTED_EXTENSIONS     = ('jpg', 'jpeg', 'tif', 'tiff', 'png')     # Accepted file extensions
CROP_DIRECTORY_PATH     = '\\Cropped_Images'                        # Cropped images path
HU_DIRECTORY_PATH       = '\\HU'                                    # HU files path

# Global Variables
topx, topy, botx, boty = 0, 0, 0, 0

class ChooseArea(Toplevel):
    """
    Class for object of choose area of tkinter app
    """
    
    def __init__(self, dir_path, image_name):
        """
        Initialization function for choose area window
        
        Parameters:
            self        - current object
            dir_path    - path to images directory
            image_name  - current image name
            
        Return:
            None
        """
        
        super(ChooseArea, self).__init__()
        
        # Initialize attributes
        self.dir_path = dir_path
        self.image_name = image_name
        
        # Open the image and get size of the image
        self.image = Image.open(self.dir_path + "\\" + self.image_name)
        self.width, self.height = self.image.width, self.image.height
        
        # Prepare the window
        self.title("Select Area")
        self.geometry('%sx%s' % (self.width, self.height))
        self.configure(background='grey')
        self.resizable(False,False)
        
        # Place the image inside the canvas
        self.img = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self, width=self.img.width(), height=self.img.height(),
                           borderwidth=0, highlightthickness=0)
        
        # Set the canvas location in the window
        self.canvas.grid(row=0,column=0)
        self.canvas.img = self.img  # Keep reference in case this code is put into a function.
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        
        # Create selection rectangle (invisible since corner points are equal).
        self.rect_id = self.canvas.create_rectangle(topx, topy, topx, topy,
                                          dash=(2,2), fill='', outline='white')
        
        # Mouse events
        self.canvas.bind('<Button-1>', self.get_mouse_posn)
        self.canvas.bind('<B1-Motion>', self.update_sel_rect)
        self.canvas.bind('<Button-2>', self.update_release)
        
    def get_mouse_posn(self, event):
        """
        the function saves the start mouse position according to mouse click location
        
        Parameters:
            self  - current object
            event - mouse click event
            
        Return:
            None
        """
        global topy, topx
        
        # Get click location
        topx, topy = event.x, event.y

    def update_sel_rect(self, event):
        """
        the function performs save of the rectangle from start to end point
        
        Parameters:
            self  - current object
            event - mouse click event
            
        Return:
            None
        """
        global topy, topx, botx, boty
    
        # Check if event is inside window
        if (((event.x <= self.width) and 
             (event.y <= self.height)) and
            ((event.x >=0) and
             (event.y >= 0))):
            # Save the end location of the rectangle
            botx, boty = event.x, event.y
            
            # Redraw the rectangle according to mouse location
            self.canvas.coords(self.rect_id, topx, topy, botx, boty)  # Update selection rect.
    
    def update_release(self, event):
        """
        the function creates mask from selected area and clean the outside area from all pictures in the directory
        
        Parameters:
            self  - current object
            event - mouse click event
            
        Return:
            None
        """
        
        # Create empty mask matrix
        mask = np.zeros(self.image.size[:2], dtype="uint8")
        
        # find high and low values of x
        if (topx <= botx):
            startLocX = topx
            endLocX = botx
        else:
            startLocX = botx
            endLocX = topx
            
        # find high and low values of y
        if (topy <= boty):
            startLocY = topy
            endLocY = boty
        else:
            startLocY = boty
            endLocY = topy
        
        # Run over the pixels inside the chosen rectangle
        for x in range(startLocX, (endLocX - 1)):
            # Run over the columns inside the rectangle
            for y in range(startLocY, (endLocY - 1)):
                # Set the pixel as white - chosen area
                mask[y][x] = 255   
        
        # Run the corp of the area on all images in the path
        self.cropImages(self.dir_path, mask)
    
    def cropImages(self, path, mask):
        """
        the function crops and saves the images according to selected mask.
        
        Parameters:
            self  - current object
            path  - path of images directory
            mask  - mask to crop images
            
        Return:
            None
        """
        
        # Load all files in directory to array - without directories
        lstOnlyWantedFilesInDir = [f for f in listdir(path) if isfile(join(path, f)) and f.lower().endswith(ACCEPTED_EXTENSIONS)]
        
        # Create path to crop images directory
        strCropPath = path + CROP_DIRECTORY_PATH
        
        # Check if the directory of cropped images exists
        boolCropDirExists = Path(strCropPath).exists()
        
        # Check if backup directory not exists
        if (not boolCropDirExists):
            os.mkdir(strCropPath)
        
        # Run over images in directory
        for img in lstOnlyWantedFilesInDir:
            # Open current image
            curImage = cv2.imread(path + "\\" + img)
    
            # Check if shape of image is same to mask
            if (curImage.shape[:2] == mask.shape):
                # Convert the image to gray
                imagegray = cv2.cvtColor(curImage,cv2.COLOR_BGR2GRAY)
                
                # Perform bitwise and operation between the CT image and the mask to get only wanted area
                masked = cv2.bitwise_and(imagegray, mask)
                
                # Convert back to rgb
                backtorgb = cv2.cvtColor(masked, cv2.COLOR_GRAY2RGB)
                
                # Save the cropped image in the directory
                cv2.imwrite(strCropPath + "\\" + img, backtorgb)
        
        # Check if HU directory exists if yes the files converted from dicom therefore copy the dir
        boolHUDirExists = Path(path + HU_DIRECTORY_PATH).exists()
        
        # Check if directory exists
        if (boolHUDirExists):
            # Check if HU directory exists in crop dir
            boolCropHUDirExists = Path(strCropPath + HU_DIRECTORY_PATH).exists()
            
            # Check if not exists
            if (not boolCropHUDirExists):
                # Copy the HU dir to cropped images path
                copytree(path + HU_DIRECTORY_PATH, strCropPath + HU_DIRECTORY_PATH)
        
        # Show message about successful crop
        messagebox.showinfo(title="Crop completed!", message="Crop of all images completed!")
        
        # Close the window
        self.destroy()