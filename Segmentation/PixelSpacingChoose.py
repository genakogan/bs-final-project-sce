# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk

# Constant variable definition
WINDOW_HEIGHT           = 200           # The height of the main window
WINDOW_WIDTH            = 100           # The width of the main window
INDEX_X                 = 0             # Index of x spacing in the list
INDEX_Y                 = 1             # Index of y spacing in the list
INDEX_Z                 = 2             # Index of z spacing in the list
SPACIMG_RESOLUTION      = 0.0001        # Increment resolution for spacing

# Global
results = []

class PixelSpaceChoose(Toplevel):
    """
    Class for object of pixel spacing choose type of tkinter app
    """
    
    def __init__(self, lstSpace):
        """
        Initialization function for pixel spacing choose window
        
        Parameters:
            self - current object
            
        Return:
            None
        """
        
        super(PixelSpaceChoose, self).__init__()
        
        # Disable resize of the window
        self.resizable(False, False)
        
        # Set title for the window
        self.title("Pixel Spacing Select")
        self.minsize(WINDOW_HEIGHT, WINDOW_WIDTH)
        
        # Create frame for sliders
        self.slidersFrame = Frame(self)
        self.slidersFrame.grid(row = 0, column = 0)
        
        # Create frame for button
        self.buttonFrame = Frame(self)
        self.buttonFrame.grid(row = 1, column = 0)
        
        # Define variablies to hold data in silders and spinboxes
        varX = DoubleVar(value = lstSpace[INDEX_X])
        varY = DoubleVar(value = lstSpace[INDEX_Y])
        varZ = DoubleVar(value = lstSpace[INDEX_Z])
        
        # Add sliders for X spacing options:
        self.xSpacingLbl = Label(self.slidersFrame, text="X spacing:").grid(row=0,padx=20, sticky=W)
        self.xSpacing = Scale(self.slidersFrame, showvalue=0, from_=0, to=1, resolution = SPACIMG_RESOLUTION, orient=HORIZONTAL, variable=varX)
        self.xSpacing.grid(row = 0, column = 1, sticky='w')
        
        # Add textbox for X spinbox
        self.tbXSpacing = Spinbox(self.slidersFrame, textvariable=varX, wrap=True, width=10, from_=0, to=1, increment = SPACIMG_RESOLUTION)
        self.tbXSpacing.grid(row = 0, column = 2,rowspan=1, sticky='WE')
        
        # Add sliders for Y spacing options:
        self.ySpacingLbl = Label(self.slidersFrame, text="Y spacing:").grid(row=1,padx=20, sticky=W)
        self.ySpacing = Scale(self.slidersFrame, showvalue=0, from_=0, to=1, resolution = SPACIMG_RESOLUTION, orient=HORIZONTAL, variable=varY)
        self.ySpacing.grid(row = 1, column = 1, sticky='w')
        
        # Add textbox for Y spinbox
        self.tbYSpacing = Spinbox(self.slidersFrame, textvariable=varY, wrap=True, width=10, from_=0, to=1, increment = SPACIMG_RESOLUTION)
        self.tbYSpacing.grid(row = 1, column = 2,rowspan=1, sticky='WE')
        
        # Add sliders for Z spacing options:
        self.zSpacingLbl = Label(self.slidersFrame, text="Z spacing:").grid(row=2,padx=20, sticky=W)
        self.zSpacing = Scale(self.slidersFrame, showvalue=0, from_=0, to=1, resolution = SPACIMG_RESOLUTION, orient=HORIZONTAL, variable=varZ)
        self.zSpacing.grid(row = 2, column = 1, sticky='w')
        
        # Add textbox for Y spinbox
        self.tbZSpacing = Spinbox(self.slidersFrame, textvariable=varZ, wrap=True, width=10, from_=0, to=1, increment = SPACIMG_RESOLUTION)
        self.tbZSpacing.grid(row = 2, column = 2,rowspan=1, sticky='WE')
        
        # Add button for save
        self.btnSave = ttk.Button(self.buttonFrame, text="Save", command=self.saveOptions)
        self.btnSave.config(width=int(WINDOW_WIDTH / 4))
        self.btnSave.grid(column = 0, row = 0, pady = 10)
        
    def saveOptions(self):
        """
        The function saves the selected values into result list
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Global results list
        global results
        
        # Save the wanted items into results list
        results = [float(self.tbXSpacing.get()), float(self.tbYSpacing.get()), float(self.tbZSpacing.get())]
        
        # Close the menu
        self.destroy()
        
        
# Run the main GUI
#root = PixelSpaceChoose()
#root.mainloop()